# from urllib.parse import urlencode
# import pytest
# from icecream import ic
# from app.core.settings import settings
# from tests.helpers import setup_product_data
# from tests.helpers import validate_datetime
# # POST - CREATE
# @pytest.mark.anyio
# async def test_create_normal_products_should_return_201_POST(client, session, factory_product, admin_user_token):
#     response = await client.post(
#         f"{settings.base_product_route}/",
#         json={"name": factory_product.name, "description": factory_product.description},
#         headers=admin_user_token,
#     )
#     response_json = response.json()
#     assert response.status_code == 201
#     assert response_json["name"] == factory_product.name
#     assert response_json["description"] == factory_product.description
#     assert validate_datetime(response_json["created_at"])
#     assert validate_datetime(response_json["updated_at"])
# @pytest.mark.anyio
# async def test_create_normal_product_should_return_422_unprocessable_entity_POST(client, session, admin_user_token):
#     response = await client.post(f"{settings.base_product_route}/", headers=admin_user_token)
#     assert response.status_code == 422
# @pytest.mark.anyio
# async def test_create_normal_product_should_return_409_email_already_registered_POST(
#     client, session, admin_user_token, product
# ):
#     response = await client.post(
#         f"{settings.base_product_route}/",
#         json={"name": product.name, "description": product.description},
#         headers=admin_user_token,
#     )
#     assert response.status_code == 409
#     assert response.json() == {"detail": "Product already registered"}
# @pytest.mark.anyio
# async def test_create_product_should_return_409_email_already_registered_POST(
#     client, session, admin_user_token, product
# ):
#     response = await client.post(
#         f"{settings.base_product_route}/",
#         json={"name": product.name, "description": product.description},
#         headers=admin_user_token,
#     )
#     assert response.status_code == 409
#     assert response.json() == {"detail": "Product already registered"}
# # GET - ALL
# @pytest.mark.anyio
# async def test_get_all_products_should_return_200_OK_GET(
#     session, client, default_created_search_options, normal_user_token
# ):
#     default_created_search_options["ordering"] = "-name"
#     await setup_product_data(session, product_qty=8)
#     response = await client.get(
#         f"{settings.base_product_route}/?{urlencode(default_created_search_options)}", headers=normal_user_token
#     )
#     response_json = response.json()
#     response_founds = response_json["founds"]
#     assert response.status_code == 200
#     assert len(response_founds) == 8
#     assert response_json["search_options"] == default_created_search_options | {"total_count": 8}
#     assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
#     assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])
# @pytest.mark.anyio
# async def test_get_all_products_with_page_size_should_return_200_OK_GET(session, client, normal_user_token):
#     query_find_parameters = {"ordering": "id", "page": 1, "page_size": 5}
#     await setup_product_data(session, 5)
#     response = await client.get(
#         f"{settings.base_product_route}/?{urlencode(query_find_parameters)}", headers=normal_user_token
#     )
#     response_json = response.json()
#     response_founds = response_json["founds"]
#     assert response.status_code == 200
#     assert len(response_founds) == 5
#     assert response_json["search_options"] == query_find_parameters | {"total_count": 5}
#     assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
#     assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])
# @pytest.mark.anyio
# async def test_get_all_products_with_pagination_should_return_200_OK_GET(session, client, normal_user_token):
#     query_find_parameters = {"ordering": "id", "page": 2, "page_size": 4}
#     await setup_product_data(session, 8)
#     response = await client.get(
#         f"{settings.base_product_route}/?{urlencode(query_find_parameters)}", headers=normal_user_token
#     )
#     response_json = response.json()
#     response_founds = response_json["founds"]
#     assert response.status_code == 200
#     assert len(response_founds) == query_find_parameters["page_size"]
#     assert response_json["search_options"] == query_find_parameters | {
#         "total_count": query_find_parameters["page_size"]
#     }
#     assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
#     assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])
# # DELETE
# @pytest.mark.anyio
# async def test_delete_product_should_return_204_OK_DELETE(session, client, admin_user_token, product):
#     response = await client.delete(f"{settings.base_product_route}/{product.id}", headers=admin_user_token)
#     get_products_response = await client.get(f"{settings.base_product_route}/", headers=admin_user_token)
#     assert response.status_code == 204
#     assert get_products_response.status_code == 200
#     assert len(get_products_response.json()["founds"]) == 0
# @pytest.mark.anyio
# async def test_delete_product_should_return_403_FORBIDDEN_DELETE(session, client, normal_user_token, product):
#     response = await client.delete(f"{settings.base_product_route}/{product.id}", headers=normal_user_token)
#     response_json = response.json()
#     get_products_response = await client.get(f"{settings.base_product_route}/", headers=normal_user_token)
#     assert response.status_code == 403
#     assert response_json == {"detail": "Not enough permissions"}
#     assert get_products_response.status_code == 200
#     assert len(get_products_response.json()["founds"]) == 1
# # GET - BY ID
# @pytest.mark.anyio
# async def test_get_product_by_id_should_return_200_OK_GET(session, client, product):
#     response = await client.get(f"{settings.base_product_route}/{product.id}")
#     response_json = response.json()
#     assert response.status_code == 200
#     assert response_json["name"] == product.name
#     assert response_json["description"] == product.description
#     assert validate_datetime(response_json["created_at"])
#     assert validate_datetime(response_json["updated_at"])
# @pytest.mark.anyio
# async def test_get_product_by_id_should_return_404_NOT_FOUND_GET(session, client, random_uuid):
#     response = await client.get(f"{settings.base_product_route}/{random_uuid}")
#     assert response.status_code == 404
#     assert response.json() == {"detail": f"id not found: {random_uuid}"}
# # PUT
# @pytest.mark.anyio
# async def test_put_product_should_return_200_OK_PUT(session, client, factory_product, product, admin_user_token):
#     different_product = {
#         "name": factory_product.name,
#         "description": factory_product.description,
#     }
#     response = await client.put(
#         f"{settings.base_product_route}/{product.id}", headers=admin_user_token, json=different_product
#     )
#     response_json = response.json()
#     assert response.status_code == 200
#     assert validate_datetime(response_json["created_at"])
#     assert validate_datetime(response_json["updated_at"])
#     assert all([response_json[key] == value for key, value in different_product.items()])
# @pytest.mark.anyio
# async def test_put_other_id_product_should_return_404_NOT_FOUND_PUT(
#     session, client, factory_product, product, admin_user_token, random_uuid
# ):
#     different_product = {
#         "name": product.name,
#         "description": product.description,
#     }
#     response = await client.put(
#         f"{settings.base_product_route}/{random_uuid}", headers=admin_user_token, json=different_product
#     )
#     response_json = response.json()
#     assert response.status_code == 404
#     assert response_json == {"detail": f"id not found: {random_uuid}"}
# @pytest.mark.anyio
# async def test_put_same_product_should_return_400_BAD_REQUEST_PUT(session, client, product, admin_user_token):
#     different_product = {
#         "name": product.name,
#         "description": product.description,
#     }
#     response = await client.put(
#         f"{settings.base_product_route}/{product.id}", headers=admin_user_token, json=different_product
#     )
#     response_json = response.json()
#     assert response.status_code == 400
#     assert response_json == {"detail": "No changes detected"}
# @pytest.mark.anyio
# async def test_put_product_should_return_403_FORBIDDEN(session, client, factory_product, product, normal_user_token):
#     different_product = {
#         "name": factory_product.name,
#         "description": factory_product.description,
#     }
#     response = await client.put(
#         f"{settings.base_product_route}/{product.id}", headers=normal_user_token, json=different_product
#     )
#     assert response.json() == {"detail": "Not enough permissions"}
#     assert response.status_code == 403
# ic
