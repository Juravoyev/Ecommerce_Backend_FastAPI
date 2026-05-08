import pytest


@pytest.mark.asyncio
async def test_buyer_cannot_create_product(client):

    # register buyer
    await client.post(
        "/auth/register",
        json={
            "username": "buyer1",
            "email": "buyer@gmail.com",
            "password": "12345"
        }
    )

    # login
    login_response = await client.post(
        "/auth/login",
        data={
            "username": "buyer1",
            "password": "12345"
        }
    )

    token = login_response.json()["access_token"]

    # create product
    response = await client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        data={
            "title": "Phone",
            "description": "Good phone",
            "price": 500,
            "category_id": 1
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_without_token(client):

    response = await client.delete(
        "/products/1"
    )

    assert response.status_code == 401
