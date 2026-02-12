#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="user-auth-smoke"
source "$(dirname "$0")/stack-lib.sh"

require_backend_health

EMAIL="smoke+$(date +%s)@example.com"
PASSWORD="Passw0rd123!"

register_resp=$(curl -fsS -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
log "Registered user: $EMAIL"

token=$(extract_access_token <<<"$register_resp")
if [ -z "$token" ]; then
  log "No token from register, trying login..."
  login_resp=$(curl -fsS -X POST http://127.0.0.1:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
  token=$(extract_access_token <<<"$login_resp")
fi

if [ -z "$token" ]; then
  echo "Could not obtain access token from register/login response."
  echo "register response: $register_resp"
  exit 1
fi

curl -fsS http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer $token" >/dev/null
log "Verified /me endpoint."

write_smoke_context "$EMAIL" "$PASSWORD" "$token"
log "User auth smoke test OK"
