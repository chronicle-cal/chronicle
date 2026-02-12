#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="${LOG_LABEL:-test}"
SMOKE_CONTEXT_FILE="${SMOKE_CONTEXT_FILE:-/tmp/chronicle-smoke-user.env}"

log() {
  echo "[$LOG_LABEL] $1"
}

init_compose_cmd() {
  if command -v podman-compose >/dev/null 2>&1; then
    COMPOSE_CMD=(podman-compose -f compose.yaml)
  else
    echo "podman-compose is not available."
    exit 1
  fi
}

wait_for_backend_health() {
  local max_tries="${1:-45}"
  log "Waiting for backend health..."
  for _ in $(seq 1 "$max_tries"); do
    if curl -fsS http://127.0.0.1:8000/api/health >/dev/null; then
      log "Backend is healthy."
      return 0
    fi
    sleep 2
  done

  log "Backend did not become healthy in time."
  return 1
}

start_backend_stack_and_wait() {
  init_compose_cmd
  log "Starting postgres+backend..."
  "${COMPOSE_CMD[@]}" up -d --build postgres backend
  log "Backend start command executed."
  wait_for_backend_health 45
}

require_backend_health() {
  if ! curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    echo "Backend is not running. Run backend-start-health test first."
    return 1
  fi
}

extract_access_token() {
  python3 -c 'import json,sys; print(json.load(sys.stdin).get("access_token", ""))'
}

write_smoke_context() {
  local email="$1"
  local password="$2"
  local token="$3"
  mkdir -p "$(dirname "$SMOKE_CONTEXT_FILE")"
  printf "EMAIL=%q\nPASSWORD=%q\nTOKEN=%q\n" "$email" "$password" "$token" >"$SMOKE_CONTEXT_FILE"
  log "Wrote smoke context to $SMOKE_CONTEXT_FILE"
}

load_smoke_context() {
  if [ ! -f "$SMOKE_CONTEXT_FILE" ]; then
    echo "Smoke context file not found: $SMOKE_CONTEXT_FILE"
    return 1
  fi
  source "$SMOKE_CONTEXT_FILE"
}

clear_db_state() {
  init_compose_cmd
  log "Clearing stack and database volumes..."
  "${COMPOSE_CMD[@]}" down -v --remove-orphans >/dev/null 2>&1 || true
  rm -f "$SMOKE_CONTEXT_FILE"
  log "Database cleanup done."
}
