import pytest
from httpx import AsyncClient
from tests.utils import register_user, login_user, auth_headers


@pytest.mark.asyncio
async def test_auth_full_lifecycle(client: AsyncClient):
    email, pwd = "full@test.com", "SecurePass123!"
    await register_user(client, email, pwd)

    login_resp = await login_user(client, email, pwd)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = auth_headers(token)

    me_resp = await client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == email

    """
    upd_name = await client.post(
        "/api/auth/update-name",
        json={"name": "New Name", "password": pwd},
        headers=headers,
    )
    assert upd_name.status_code == 200

    await client.post(
        "/api/auth/update-name",
        json={"name": "Second Name", "password": pwd},
        headers=headers,
    )

    new_email = "new_full@test.com"
    bad_email = await client.post(
        "/api/auth/update-email",
        json={"new_email": email, "password": pwd},
        headers=headers,
    )
    assert bad_email.status_code == 400

    email_upd = await client.post(
        "/api/auth/update-email",
        json={"new_email": new_email, "password": pwd},
        headers=headers,
    )
    assert email_upd.status_code == 200
    new_token = email_upd.json()["access_token"]
    new_headers = auth_headers(new_token)

    new_pwd = "EvenSafer456!"
    pwd_upd = await client.post(
        "/api/auth/update-password",
        json={"current_password": pwd, "new_password": new_pwd},
        headers=new_headers,
    )
    assert pwd_upd.status_code == 200
    """


@pytest.mark.asyncio
async def test_auth_errors_and_edge_cases(client: AsyncClient):
    email, pwd = "dup@test.com", "Pass123!"
    await register_user(client, email, pwd)
    res = await client.post(
        "/api/auth/register", json={"email": email, "password": pwd}
    )
    assert res.status_code == 409

    bad_login = await login_user(client, email, "wrongPass123!")
    assert bad_login.status_code == 401

    assert (
        await client.get(
            "/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"}
        )
    ).status_code == 401
    assert (
        await client.get("/api/auth/me", headers={"Authorization": "Bearer nopoint"})
    ).status_code == 401


"""
@pytest.mark.asyncio
async def test_delete_account_flow(client: AsyncClient):
    email, pwd = "delete@test.com", "Pass123!"
    user = await register_user(client, email, pwd)
    headers = auth_headers(user["access_token"])

    bad_del = await client.post(
        "/api/auth/delete-account", json={"confirm": "no"}, headers=headers
    )
    assert bad_del.status_code == 400

    ok_del = await client.post(
        "/api/auth/delete-account", json={"confirm": "delete"}, headers=headers
    )
    assert ok_del.status_code == 200

    res = await client.get("/api/auth/me", headers=headers)
    assert res.status_code == 401
    assert res.json()["detail"] == "User not found"
"""


@pytest.mark.asyncio
async def test_logout_endpoint(client: AsyncClient):
    resp = await client.post("/api/auth/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "logged out"
