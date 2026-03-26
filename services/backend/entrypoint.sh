#!/bin/sh
alembic upgrade head
exec "$@"
