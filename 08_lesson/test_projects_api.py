import pytest

PROJECTS_URL = "api-v2/projects"


def test_create_project_positive(api_client, base_url):
    payload = {
        "title": "Test Project - Auto Created",
        "users": {},
    }
    response = api_client.post(f"{base_url}/{PROJECTS_URL}", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_all_projects(api_client, base_url):
    response = api_client.get(f"{base_url}/{PROJECTS_URL}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert isinstance(data["content"], list)


def test_get_project_by_id(api_client, base_url):
    create_payload = {"title": "Temp Project", "users": {}}
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}", json=create_payload
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]
    get_response = api_client.get(
        f"{base_url}/{PROJECTS_URL}/{project_id}"
    )
    assert get_response.status_code == 200
    assert get_response.json()["id"] == project_id


def test_update_project_name(api_client, base_url):
    create_payload = {"title": "Project to Update", "users": {}}
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}", json=create_payload
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]
    update_payload = {"title": "Updated Name"}
    update_response = api_client.put(
        f"{base_url}/{PROJECTS_URL}/{project_id}",
        json=update_payload,
    )
    assert update_response.status_code == 200


def test_delete_project(api_client, base_url):
    create_payload = {"title": "Project to Delete", "users": {}}
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}", json=create_payload
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]
    delete_response = api_client.delete(
        f"{base_url}/{PROJECTS_URL}/{project_id}"
    )
    if delete_response.status_code == 404:
        delete_response = api_client.put(
            f"{base_url}/{PROJECTS_URL}/{project_id}",
            json={"deleted": True},
        )
    assert delete_response.status_code in [200, 204]


@pytest.mark.parametrize("invalid_name", ["", None])
def test_create_project_negative_invalid_name(api_client, base_url, invalid_name):
    payload = {"title": invalid_name, "users": {}}
    response = api_client.post(f"{base_url}/{PROJECTS_URL}", json=payload)
    assert response.status_code in [400, 422], (
        f"Ожидался статус 400/422 при неверном имени, "
        f"получен {response.status_code}"
    )