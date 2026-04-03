import pytest
import uuid

class TestProjectsAPI:
    PROJECTS_URL = "/api-v2/projects"

    def _create_test_project(self, api_client, base_url):
        """Вспомогательная функция для создания тестового проекта"""
        project_name = f"Test Project {uuid.uuid4().hex[:8]}"
        payload = {
            "name": project_name,
            "description": "Автоматизированный тест создания проекта"
        }
        response = api_client.post(f"{base_url}{self.PROJECTS_URL}", json=payload)
        assert response.status_code == 201, f"Создание проекта не удалось: {response.text}"
        return response.json()

    @pytest.fixture
    def created_project(self, api_client, base_url):
        """Фикстура для создания и очистки тестового проекта"""
        project = self._create_test_project(api_client, base_url)
        yield project
        # Очистка после теста — попытка удалить проект, игнорируем ошибки 404
        try:
            delete_response = api_client.delete(f"{base_url}{self.PROJECTS_URL}/{project['id']}")
            if delete_response.status_code not in [200, 204, 404]:
                print(f"Предупреждение: не удалось удалить проект {project['id']}: {delete_response.text}")
        except Exception as e:
            print(f"Ошибка при удалении проекта {project['id']}: {e}")

    def test_create_project_positive(self, api_client, base_url):
        """Позитивный тест: создание проекта с корректными данными"""
        project_data = self._create_test_project(api_client, base_url)

        # Проверки
        assert "id" in project_data, "В ответе отсутствует поле 'id'"
        assert len(project_data["id"]) > 0, "ID проекта пуст"
        assert project_data["name"] is not None, "Имя проекта отсутствует"
        assert project_data["description"] == "Автоматизированный тест создания проекта", "Описание не совпадает"

    def test_create_project_negative_missing_name(self, api_client, base_url):
        """Негативный тест: попытка создания проекта без обязательного поля 'name'"""
        payload = {"description": "Проект без названия"}

        response = api_client.post(f"{base_url}{self.PROJECTS_URL}", json=payload)

        assert response.status_code in [400, 422], f"Ожидался 400 или 422, получен {response.status_code}: {response.text}"
        response_data = response.json()
        error_message = str(response_data).lower()
        assert any(keyword in error_message for keyword in ["name", "required", "обязательное"]), \
            f"В ответе нет указания на отсутствие поля 'name': {response_data}"

    @pytest.mark.parametrize("invalid_name", ["", "   ", "a" * 256])
    def test_create_project_negative_invalid_name_values(self, api_client, base_url, invalid_name):
        """Негативный тест: проверка различных некорректных значений для поля 'name'"""
        payload = {
            "name": invalid_name,
            "description": "Проект с некорректным именем"
        }

        response = api_client.post(f"{base_url}{self.PROJECTS_URL}", json=payload)
        assert response.status_code in [400, 422], \
            f"Ожидался 400/422 для '{invalid_name}', получен {response.status_code}: {response.text}"

    def test_update_project_positive(self, api_client, base_url, created_project):
        """Позитивный тест: обновление существующего проекта"""
        project_id = created_project["id"]
        updated_name = f"Updated Project {uuid.uuid4().hex[:8]}"
        update_payload = {
            "name": updated_name,
            "description": "Обновлённое описание проекта"
        }

        response = api_client.put(
            f"{base_url}{self.PROJECTS_URL}/{project_id}",
            json=update_payload
        )

        assert response.status_code == 200, f"Ожидался 200 OK, получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["name"] == updated_name, f"Имя не обновилось: ожидалось '{updated_name}', получено '{data['name']}'"
        assert data["description"] == update_payload["description"], "Описание не обновилось"

    def test_update_project_negative_nonexistent_id(self, api_client, base_url):
        """Негативный тест: попытка обновить проект с несуществующим ID"""
        nonexistent_id = "99999999-9999-9999-9999-999999999999"
        payload = {
            "name": "Nonexistent Update",
            "description": "Попытка обновления с несуществующим ID"
        }

        response = api_client.put(
            f"{base_url}{self.PROJECTS_URL}/{nonexistent_id}",
            json=payload
        )

        assert response.status_code in [400, 404], \
            f"Ожидался 400/404, получен {response.status_code}: {response.text}"

    @pytest.mark.parametrize("invalid_name", ["", "   ", "a" * 256])
    def test_update_project_negative_invalid_name(self, api_client, base_url, created_project, invalid_name):
        """Негативный тест: проверка некорректных значений для поля 'name' при обновлении"""
        project_id = created_project["id"]

        payload = {
            "name": invalid_name,
            "description": "Проект с некорректным именем"
        }

        response = api_client.put(
            f"{base_url}{self.PROJECTS_URL}/{project_id}",
            json=payload
        )

        assert response.status_code in [400, 422], \
            f"Ожидался 400/422 для '{invalid_name}', получен {response.status_code}: {response.text}"

    def test_get_project_positive(self, api_client, base_url, created_project):
        """Позитивный тест: получение данных существующего проекта"""
        project_id = created_project["id"]

        response = api_client.get(
            f"{base_url}{self.PROJECTS_URL}/{project_id}"
        )

        assert response.status_code == 200, f"Ожидался 200 OK, получен {response.status_code}: {response.text}"
        data = response.json()
        expected_fields = {"id", "name", "description"}
        assert all(field in data for field in expected_fields), \
            f"Ответ не содержит обязательных полей. Получено: {list(data.keys())}"
        assert data["id"] == project_id, f"ID не совпадает: ожидалось {project_id}, получено {data['id']}"

    def test_get_project_negative_nonexistent_id(self, api_client, base_url):
        """Негативный тест: попытка получить проект с несуществующим ID"""
        nonexistent_id = "99999999-9999-9999-9999-999999999999"

        response = api_client.get(
            f"{base_url}{self.PROJECTS_URL}/{nonexistent_id}"
        )

        assert response.status_code in [400, 404], \
            f"Ожидался 400/404, получен {response.status_code}: {response.text}"
