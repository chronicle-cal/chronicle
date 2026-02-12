#!/usr/bin/env bash
set -euo pipefail

LOG_LABEL="backend-start-health-smoke"
source "$(dirname "$0")/stack-lib.sh"

start_backend_stack_and_wait
log "Backend start+health smoke test OK"
