#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="db-reset-smoke"
source "$(dirname "$0")/stack-lib.sh"

clear_db_state
log "DB reset smoke test OK"
