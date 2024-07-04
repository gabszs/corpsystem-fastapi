from urllib.parse import urlencode

import pytest
from icecream import ic

from app.core.settings import settings
from tests.helpers import setup_inventory_data
from tests.helpers import validate_datetime


# POST - CREATE
@pytest.mark.anyio
async def test_create_normal_inventory_should_return_201_POST(
    client, session, factory_inventory, product, normal_user, admin_user_token
):
    response = await client.post(
        f"{settings.base_inventory_route}/",
        json={
            "product_id": str(product.id),
            "quantity": factory_inventory.quantity,
            "unit_price": factory_inventory.unit_price,
        },
        headers=admin_user_token,
    )
    response_json = response.json()

    assert response.status_code == 201
    assert response_json["quantity"] == factory_inventory.quantity
    assert response_json["unit_price"] == factory_inventory.unit_price
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_create_normal_inventory_should_return_422_unprocessable_entity_POST(client, session, admin_user_token):
    response = await client.post(f"{settings.base_inventory_route}/", headers=admin_user_token)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_normal_inventory_should_return_409_email_already_registered_POST(
    client, session, admin_user_token, inventory
):
    response = await client.post(
        f"{settings.base_inventory_route}/",
        json={"product_id": str(inventory.product_id), "quantity": 1, "unit_price": 1},
        headers=admin_user_token,
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Inventory already registered"}


# GET - ALL
@pytest.mark.anyio
async def test_get_all_inventory_should_return_200_OK_GET(session, client, admin_user_token):
    await setup_inventory_data(session, inventory_qty=8)
    response = await client.get(f"{settings.base_inventory_route}/", headers=admin_user_token)
    response_json = response.json()
    response_founds = response_json["founds"]

    assert response.status_code == 200
    assert len(response_founds) == 8
    assert response_json["search_options"]["total_count"] == 8
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


@pytest.mark.anyio
async def test_get_all_inventory_with_page_size_should_return_200_OK_GET(session, client, admin_user_token):
    query_find_parameters = {"ordering": "id", "page": 1, "page_size": 5}
    await setup_inventory_data(session, 5)
    response = await client.get(
        f"{settings.base_inventory_route}/?{urlencode(query_find_parameters)}", headers=admin_user_token
    )
    response_json = response.json()
    response_founds = response_json["founds"]

    assert response.status_code == 200
    assert len(response_founds) == 5
    assert response_json["search_options"] == query_find_parameters | {"total_count": 5}
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


@pytest.mark.anyio
async def test_get_all_inventory_with_pagination_should_return_200_OK_GET(session, client, admin_user_token):
    query_find_parameters = {"ordering": "id", "page": 2, "page_size": 4}
    await setup_inventory_data(session, 8)
    response = await client.get(
        f"{settings.base_inventory_route}/?{urlencode(query_find_parameters)}", headers=admin_user_token
    )
    response_json = response.json()
    response_founds = response_json["founds"]
    assert response.status_code == 200
    assert len(response_founds) == query_find_parameters["page_size"]
    assert response_json["search_options"] == query_find_parameters | {
        "total_count": query_find_parameters["page_size"]
    }
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


# # DELETE
@pytest.mark.anyio
async def test_delete_inventory_should_return_204_OK_DELETE(session, client, admin_user_token, inventory):
    response = await client.delete(f"{settings.base_inventory_route}/{inventory.id}", headers=admin_user_token)
    get_inventory_response = await client.get(f"{settings.base_inventory_route}/", headers=admin_user_token)
    assert response.status_code == 204
    assert get_inventory_response.status_code == 200
    assert len(get_inventory_response.json()["founds"]) == 0


@pytest.mark.anyio
async def test_delete_inventory_should_return_403_FORBIDDEN_DELETE(
    session, client, normal_user_token, inventory, admin_user_token
):
    response = await client.delete(f"{settings.base_inventory_route}/{inventory.id}", headers=normal_user_token)
    response_json = response.json()
    get_inventory_response = await client.get(f"{settings.base_inventory_route}/", headers=admin_user_token)
    assert response.status_code == 403
    assert response_json == {"detail": "Not enough permissions"}
    assert get_inventory_response.status_code == 200
    assert len(get_inventory_response.json()["founds"]) == 1


# # GET - BY ID
@pytest.mark.anyio
async def test_get_inventory_by_id_should_return_200_OK_GET(session, client, inventory):
    response = await client.get(f"{settings.base_inventory_route}/{inventory.id}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["quantity"] == inventory.quantity
    assert response_json["unit_price"] == inventory.unit_price
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_get_inventory_by_id_should_return_404_NOT_FOUND_GET(session, client, random_uuid):
    response = await client.get(f"{settings.base_inventory_route}/{random_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"id not found: {random_uuid}"}


# # PUT
@pytest.mark.anyio
async def test_put_inventory_should_return_200_OK_PUT(
    session, client, factory_inventory, inventory, admin_user_token, product
):
    different_inventory = {
        "product_id": str(product.id),
        "quantity": factory_inventory.quantity,
        "unit_price": factory_inventory.unit_price,
    }
    response = await client.put(
        f"{settings.base_inventory_route}/{inventory.id}", headers=admin_user_token, json=different_inventory
    )
    response_json = response.json()

    assert response.status_code == 200
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])
    assert all([response_json[key] == value for key, value in different_inventory.items()])


@pytest.mark.anyio
async def test_put_other_id_inventory_should_return_404_NOT_FOUND_PUT(
    session, client, inventory, admin_user_token, random_uuid
):
    different_inventory = {
        "product_id": str(random_uuid),
        "quantity": inventory.quantity,
        "unit_price": inventory.unit_price,
    }
    response = await client.put(
        f"{settings.base_inventory_route}/{random_uuid}", headers=admin_user_token, json=different_inventory
    )
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": f"id not found: {random_uuid}"}


@pytest.mark.anyio
async def test_put_same_inventory_should_return_400_BAD_REQUEST_PUT(session, client, inventory, admin_user_token):
    different_inventory = {
        "product_id": str(inventory.product_id),
        "quantity": inventory.quantity,
        "unit_price": inventory.unit_price,
    }
    response = await client.put(
        f"{settings.base_inventory_route}/{inventory.id}", headers=admin_user_token, json=different_inventory
    )
    response_json = response.json()
    assert response.status_code == 400
    assert response_json == {"detail": "No changes detected"}


@pytest.mark.anyio
async def test_put_inventory_should_return_403_FORBIDDEN(
    session, client, factory_inventory, inventory, normal_user_token, random_uuid
):
    different_inventory = {
        "product_id": str(random_uuid),
        "quantity": factory_inventory.quantity,
        "unit_price": factory_inventory.unit_price,
    }
    response = await client.put(
        f"{settings.base_inventory_route}/{inventory.id}", headers=normal_user_token, json=different_inventory
    )
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.status_code == 403


ic
