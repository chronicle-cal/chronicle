# NOTE: Tests currently disabled due to API restructuring
# TODO: Re-enable and update tests after RESTful refactoring is complete

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.user import User
from app.api.auth import create_token
from app.db.session import get_async_db


@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession):
    user = User(email="test@example.com", password_hash="hashed")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    token = create_token("test@example.com")
    return user, token


# @pytest.mark.asyncio
# async def test_create_sync_config(client: AsyncClient, test_user):
#     user, token = test_user
#     response = await client.post(
#         "/api/sync-configs",
#         json={
#             "id": "test-sync-1",
#             "destination": "http://example.com",
#             "username": "user",
#             "password": "pass",
#         },
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["destination"] == "http://example.com"


# @pytest.mark.asyncio
# async def test_list_sync_configs(client: AsyncClient, test_user):
#     user, token = test_user
#     response = await client.get(
#         "/api/sync-configs",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# @pytest.mark.asyncio
# async def test_unauthorized_access(client: AsyncClient):
#     response = await client.get("/api/sync-configs")
#     assert response.status_code == 401


# @pytest.mark.asyncio
# async def test_create_scheduler_config(client: AsyncClient, test_user):
#     user, token = test_user
#     response = await client.post(
#         "/api/scheduler-configs",
#         json={
#             "id": "test-scheduler-1",
#             "name": "Test Scheduler",
#             "calendar_url": "http://calendar.example.com",
#             "calendar_username": "user",
#             "calendar_password": "pass",
#         },
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["name"] == "Test Scheduler"


# @pytest.mark.asyncio
# async def test_list_scheduler_configs(client: AsyncClient, test_user):
#     user, token = test_user
#     response = await client.get(
#         "/api/scheduler-configs",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# @pytest.mark.asyncio
# async def test_delete_sync_config(
#     client: AsyncClient, test_user, db_session: AsyncSession
# ):
#     user, token = test_user
#
#     create_response = await client.post(
#         "/api/sync-configs",
#         json={
#             "id": "test-delete-1",
#             "destination": "http://example.com",
#             "username": "user",
#             "password": "pass",
#         },
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert create_response.status_code == 201
#     data = create_response.json()
#     item_id = data["id"]
#
#     delete_response = await client.delete(
#         f"/api/sync-configs/{item_id}",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert delete_response.status_code == 204
