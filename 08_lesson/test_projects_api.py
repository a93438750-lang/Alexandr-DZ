import pytest

PROJECTS_URL = "/api-v2/projects"



class TestProjectsAPI:
    """Тесты для работы с проектами через API."""

    def test_create_project_positive(self, api_client, base_url):
        """Тест создания проекта с корректными данными."""
        payload = {"name": "Test Project - Auto Created"}
        response = api_client.post(
            f"{base_url}{PROJECTS_URL}",
            json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )
        response_data = response.json()
        assert "id" in response_data, "В ответе отсутствует поле 'id'"
        assert response_data["name"] == payload["name"], "Имя проекта не совпадает"

    def test_get_all_projects(self, api_client, base_url):
        """Тест получения списка проектов."""
        response = api_client.get(f"{base_url}{PROJECTS_URL}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )
        projects = response.json()
        assert isinstance(projects, list), "Ответ должен быть списком проектов"

    def test_get_project_by_id(self, api_client, base_url):
        """Тест получения проекта по ID."""
        # Сначала создаём проект
        create_payload = {"name": "Temp Project for Get Test"}
        create_response = api_client.post(
            f"{base_url}{PROJECTS_URL}",
            json=create_payload
        )
        assert create_response.status_code == 200
        project_id = create_response.json()["id"]

        # Затем получаем его по ID
        get_response = api_client.get(
            f"{base_url}{PROJECTS_URL}/{project_id}"
        )

        assert get_response.status_code == 200, (
            f"Ожидался статус 200, получен {get_response.status_code}"
        )
        project_data = get_response.json()
        assert project_data["id"] == project_id, "ID проекта не совпадает"
        assert project_data["name"] == create_payload["name"], "Имя проекта не совпадает"

    def test_update_project_name(self, api_client, base_url):
        """Тест обновления имени проекта."""
        # Создаём проект
        create_payload = {"name": "Project to Update"}
        create_response = api_client.post(
            f"{base_url}{PROJECTS_URL}",
            json=create_payload
        )
        assert create_response.status_code == 200
        project_id = create_response.json()["id"]

        # Обновляем имя
        update_payload = {"name": "Updated Project Name"}
        update_response = api_client.put(
            f"{base_url}{PROJECTS_URL}/{project_id}",
            json=update_payload
        )

        assert update_response.status_code == 200, (
            f"Ожидался статус 200, получен {update_response.status_code}"
        )
        updated_data = update_response.json()
        assert updated_data["name"] == update_payload["name"], "Имя не обновилось"

    def test_delete_project(self, api_client, base_url):
        """Тест удаления проекта."""
        # Создаём проект для удаления
        create_payload = {"name": "Project to Delete"}
        create_response = api_client.post(
            f"{base_url}{PROJECTS_URL}",
            json=create_payload
        )
        assert create_response.status_code == 200
        project_id = create_response.json()["id"]

        # Удаляем проект
        delete_response = api_client.delete(
            f"{base_url}{PROJECTS_URL}/{project_id}"
        )

        assert delete_response.status_code == 204, (
            f"Ожидался статус 204, получен {delete_response.status_code}"
        )

    @pytest.mark.parametrize("invalid_name", ["", "   ", None])
    def test_create_project_negative_invalid_name(
        self, api_client, base_url, invalid_name
    ):
        """Негативный тест: создание проекта с некорректным именем."""
        payload = {"name": invalid_name}
        response = api_client.post(
            f"{base_url}{PROJECTS_URL}",
            json=payload
        )

        assert response.status_code in [400, 422], (
            f"Ожидался 400/422, получен {response.status_code}"
        )


