import pytest
from sqlalchemy import create_engine, text
from company_table import CompanyTable

DATABASE_URL = "postgresql://qa:skyqa@5.101.50.27:5432/x_clients"


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    return CompanyTable(DATABASE_URL)


@pytest.fixture
def cleanup(setup_database):
    yield
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("UPDATE company SET deleted_at=NULL"))
        conn.commit()


def test_add_company(setup_database, cleanup):
    new_id = setup_database.add_company(
        "Google", "Крупная технологическая компания"
    )
    added_company = setup_database.get_company_by_id(new_id)
    assert added_company is not None
    assert added_company["name"] == "Google"
    assert added_company["description"] == "Крупная технологическая компания"


def test_update_company(setup_database, cleanup):
    new_id = setup_database.add_company(
        "Google", "Крупная технологическая компания"
    )
    setup_database.update_company(
        new_id, "Alphabet Inc.", "Материнская компания Google"
    )
    updated_company = setup_database.get_company_by_id(new_id)
    assert updated_company is not None
    assert updated_company["name"] == "Alphabet Inc."
    assert updated_company["description"] == "Материнская компания Google"


def test_delete_company(setup_database, cleanup):
    new_id = setup_database.add_company(
        "Google", "Крупная технологическая компания"
    )
    setup_database.delete_company(new_id)
    deleted_company = setup_database.get_company_by_id(new_id)
    assert deleted_company is None
