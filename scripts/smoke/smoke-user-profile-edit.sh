#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="user-profile-edit-smoke"
source "$(dirname "$0")/stack-lib.sh"

require_backend_health
load_smoke_context

NEW_EMAIL="smoke-updated+$(date +%s)@example.com"
NEW_PASSWORD="Passw0rd456!"

curl -fsS -X POST http://127.0.0.1:8000/api/auth/update-name \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"name\":\"Smoke User\",\"password\":\"$PASSWORD\"}" >/dev/null
log "Updated profile name."

update_email_resp=$(curl -fsS -X POST http://127.0.0.1:8000/api/auth/update-email \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"new_email\":\"$NEW_EMAIL\",\"password\":\"$PASSWORD\"}")

TOKEN=$(extract_access_token <<<"$update_email_resp")
if [ -z "$TOKEN" ]; then
  echo "Email update did not return a token."
  echo "update-email response: $update_email_resp"
  exit 1
fi
log "Updated email to: $NEW_EMAIL"

curl -fsS -X POST http://127.0.0.1:8000/api/auth/update-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"current_password\":\"$PASSWORD\",\"new_password\":\"$NEW_PASSWORD\"}" >/dev/null
log "Updated password."

curl -fsS -X POST http://127.0.0.1:8000/api/auth/delete-account \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"confirm":"delete"}' >/dev/null
log "Deleted account."

if curl -fsS http://127.0.0.1:8000/api/auth/me -H "Authorization: Bearer $TOKEN" >/dev/null 2>&1; then
  echo "Deleted account still authenticates via /me."
  exit 1
fi
log "Verified deleted account no longer authenticates."

log "User profile edit smoke test OK"
