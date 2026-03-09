import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.profiles import router as profiles_router
from app.api.integration import profile_router
from app.core.db import Base, engine

app = FastAPI(title="Chronicle API", version="0.1.0")


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        has_calendar_source_id = await conn.execute(
            text(
                "SELECT 1 FROM information_schema.columns "
                "WHERE table_name='rules' AND column_name='calendar_source_id'"
            )
        )
        if has_calendar_source_id.first() is None:
            await conn.execute(
                text("ALTER TABLE rules ADD COLUMN calendar_source_id VARCHAR(64)")
            )

        has_calendar_profile_id = await conn.execute(
            text(
                "SELECT 1 FROM information_schema.columns "
                "WHERE table_name='rules' AND column_name='calendar_profile_id'"
            )
        )
        if has_calendar_profile_id.first() is not None:
            await conn.execute(
                text("ALTER TABLE rules ALTER COLUMN calendar_profile_id DROP NOT NULL")
            )
            missing_sources = await conn.execute(
                text(
                    "SELECT cp.id, cp.main_calendar_id "
                    "FROM calendar_profiles cp "
                    "LEFT JOIN calendar_sources cs "
                    "ON cs.profile_id = cp.id AND cs.calendar_id = cp.main_calendar_id "
                    "WHERE cp.main_calendar_id IS NOT NULL AND cs.id IS NULL"
                )
            )
            for profile_id, calendar_id in missing_sources.fetchall():
                await conn.execute(
                    text(
                        "INSERT INTO calendar_sources (id, profile_id, calendar_id) "
                        "VALUES (:id, :profile_id, :calendar_id)"
                    ),
                    {
                        "id": str(uuid.uuid4()),
                        "profile_id": profile_id,
                        "calendar_id": calendar_id,
                    },
                )

            await conn.execute(
                text(
                    "UPDATE rules r "
                    "SET calendar_source_id = cs.id "
                    "FROM calendar_sources cs "
                    "JOIN calendar_profiles cp ON cp.id = cs.profile_id "
                    "WHERE r.calendar_source_id IS NULL "
                    "AND r.calendar_profile_id = cp.id "
                    "AND cs.calendar_id = cp.main_calendar_id"
                )
            )
            await conn.execute(
                text(
                    "UPDATE rules r "
                    "SET calendar_source_id = cs.id "
                    "FROM calendar_sources cs "
                    "WHERE r.calendar_source_id IS NULL "
                    "AND r.calendar_profile_id = cs.profile_id"
                )
            )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profiles_router, prefix="/api/user-profile", tags=["user-profile"])
app.include_router(profile_router, prefix="/api/profile", tags=["calendar-profile"])
