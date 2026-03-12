#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="db-reset-smoke"
source "$(dirname "$0")/stack-lib.sh"

cleanup_smoke_users_only
log "DB smoke cleanup test OK"
