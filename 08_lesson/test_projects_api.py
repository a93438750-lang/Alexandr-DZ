import pytest

PROJECTS_URL = "api-v2/projects"


def test_create_project_positive(api_client, base_url):
    """Тест создания проекта с корректными данными."""
    payload = {
        "title": "Test Project - Auto Created",
        "users": {}
    }
    response = api_client.post(
        f"{base_url}/{PROJECTS_URL}",
        json=payload,
    )

    assert response.status_code == 201, (
        f"Ожидался статус 201, получен {response.status_code}"
    )
    response_data = response.json()
    assert "id" in response_data, "В ответе отсутствует поле 'id'"


def test_get_all_projects(api_client, base_url):
    """Тест получения списка проектов."""
    response = api_client.get(f"{base_url}/{PROJECTS_URL}")

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )
    data = response.json()
    assert isinstance(data, dict), "Ответ должен быть словарём"
    assert "content" in data, "В ответе нет ключа 'content'"
    assert isinstance(data["content"], list), "Ответ должен быть списком проектов"


def test_get_project_by_id(api_client, base_url):
    """Тест получения проекта по ID."""
    # 1. Создаем проект
    create_payload = {
        "title": "Temp Project for Get Test",
        "users": {}
    }
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}",
        json=create_payload,
    )
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    # 2. Запрашиваем по ID
    get_response = api_client.get(
        f"{base_url}/{PROJECTS_URL}/{project_id}",
    )

    assert get_response.status_code == 200, (
        f"Ожидался статус 200, получен {get_response.status_code}"
    )
    project_data = get_response.json()
    assert project_data["id"] == project_id, "ID проекта не совпадает"


def test_update_project_name(api_client, base_url):
    """Тест обновления имени проекта."""
     # 1. Создаем проект
    create_payload = {
        "title": "Project to Update",
        "users": {}
    }
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}",
        json=create_payload,
    )
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

     # 2. Обновляем имя (только поле title)
    update_payload = {
        "title": "Updated Project Name"
    }
    update_response = api_client.put(
        f"{base_url}/{PROJECTS_URL}/{project_id}",
        json=update_payload,
    )

    assert update_response.status_code == 200, (
        f"Ожидался статус 200, получен {update_response.status_code}"
    )


def test_delete_project(api_client, base_url):
    """Тест удаления проекта."""
     # Создаем проект для удаления
    create_payload = {
        "title": "Project to Delete",
        "users": {}
    }
    create_response = api_client.post(
        f"{base_url}/{PROJECTS_URL}",
        json=create_payload,
    )
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

     # Пробуем удалить через DELETE (стандарт для REST)
     # Если не сработает (404), пробуем PUT как в документации
    
     # Пробуем DELETE
    delete_response = api_client.delete(
        f"{base_url}/{PROJECTS_URL}/{project_id}",
    )
    
    # Если DELETE вернет 404, пробуем PUT из документации
    if delete_response.status_code == 404:
        update_payload = {"deleted": True}
        delete_response = api_client.put(
            f"{base_url}/{PROJECTS_URL}/{project_id}",
            json=update_payload,
        )
    
    assert delete_response.status_code in [200, 204], (
        f"Ожидался статус 200 или 204 (или 404->PUT), получен {delete_response.status_code}"
    )


@pytest.mark.parametrize("invalid_name", ["", None])
def test_create_project_negative_invalid_name(api_client, base_url, invalid_name):
     """Негативный тест: создание проекта с некорректным именем."""
     payload = {
         "title": invalid_name,
         "users": {}
     }
     response = api_client.post(
         f"{base_url}/{PROJECTS_URL}",
         json=payload,
     )
 
     assert response.status_code in [400, 422], (
         f"Ожидался статус 400/422 при неверном имени, получен {response.status_code}"
     )