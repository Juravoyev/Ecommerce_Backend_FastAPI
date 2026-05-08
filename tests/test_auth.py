import pytest


@pytest.mark.asyncio
async def test_register_user(client):

    response = await client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "12345"
        }
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_success(client):

    response = await client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):

    response = await client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
