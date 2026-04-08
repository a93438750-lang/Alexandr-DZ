import pytest
from sqlalchemy import create_engine, text  # <---- Добавь импорт create_engine
from company_table import CompanyTable

# Строка подключения к базе данных
DATABASE_URL = "postgresql://qa:skyqa@5.101.50.27:5432/x_clients"

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    global company_table
    company_table = CompanyTable(DATABASE_URL)

@pytest.fixture
def cleanup():
    yield
    engine = create_engine(DATABASE_URL)  # <---- Используй create_engine
    with engine.connect() as conn:
        conn.execute(text("UPDATE company SET deleted_at=NULL"))  # Восстанавливаем все записи

def test_add_company(cleanup):
    new_id = company_table.add_company("Google", "Крупная технологическая компания")
    added_company = company_table.get_company_by_id(new_id)
    assert added_company is not None
    assert added_company['name'] == "Google"
    assert added_company['description'] == "Крупная технологическая компания"

def test_update_company(cleanup):
    new_id = company_table.add_company("Google", "Крупная технологическая компания")
    company_table.update_company(new_id, "Alphabet Inc.", "Материнская компания Google")
    updated_company = company_table.get_company_by_id(new_id)
    assert updated_company is not None
    assert updated_company['name'] == "Alphabet Inc."
    assert updated_company['description'] == "Материнская компания Google"

def test_delete_company(cleanup):
    new_id = company_table.add_company("Google", "Крупная технологическая компания")
    company_table.delete_company(new_id)
    deleted_company = company_table.get_company_by_id(new_id)
    assert deleted_company is None