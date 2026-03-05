from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.profiles import router as profiles_router
from app.api.integration import (
    sync_config_router,
    scheduler_config_router,
    calendar_profile_router,
    rule_router,
    condition_router,
    action_router,
    task_router,
)

app = FastAPI(title="Chronicle API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profiles_router, prefix="/api/profile", tags=["profile"])

# -------------

app.include_router(sync_config_router, prefix="/api/sync-config", tags=["sync-config"])
app.include_router(
    scheduler_config_router, prefix="/api/scheduler-config", tags=["scheduler-config"]
)
app.include_router(
    calendar_profile_router, prefix="/api/calendar-profile", tags=["calendar-profile"]
)
app.include_router(rule_router, prefix="/api/rule", tags=["rule"])
app.include_router(condition_router, prefix="/api/condition", tags=["condition"])
app.include_router(action_router, prefix="/api/action", tags=["action"])
app.include_router(task_router, prefix="/api/task", tags=["task"])
