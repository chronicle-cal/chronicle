from httpx import AsyncClient


async def register_user(client: AsyncClient, email: str, password: str) -> dict:
    resp = await client.post(
        "/api/auth/register", json={"email": email, "password": password}
    )
    assert resp.status_code == 201, f"Registration failed: {resp.text}"
    return resp.json()


async def login_user(client: AsyncClient, email: str, password: str):
    resp = await client.post(
        "/api/auth/login", json={"email": email, "password": password}
    )
    return resp


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
