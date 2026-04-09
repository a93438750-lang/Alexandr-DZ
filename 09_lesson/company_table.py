from sqlalchemy import create_engine, text


class CompanyTable:
    __scripts = {
        "insert": text(
            (
                "INSERT INTO company (name, description) "
                "VALUES (:name, :description) RETURNING id"
            )
        ),
        "update": text(
            (
                "UPDATE company SET name=:new_name, "
                "description=:new_description WHERE id=:id"
            )
        ),
        "delete": text("UPDATE company SET deleted_at=NOW() WHERE id=:id"),
        "find_by_id": text(
            "SELECT * FROM company WHERE id=:id AND deleted_at IS NULL"
        ),
        "list_companies": text(
            "SELECT * FROM company WHERE deleted_at IS NULL"
        ),
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def add_company(self, name, description):
        with self.__db.connect() as conn:
            result = conn.execute(
                self.__scripts["insert"],
                {"name": name, "description": description},
            )
            new_id = result.scalar_one()
            conn.commit()
            return new_id

    def update_company(self, company_id, new_name, new_description):
        with self.__db.connect() as conn:
            conn.execute(
                self.__scripts["update"],
                {
                    "id": company_id,
                    "new_name": new_name,
                    "new_description": new_description,
                },
            )
            conn.commit()

    def delete_company(self, company_id):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["delete"], {"id": company_id})
            conn.commit()

    def get_company_by_id(self, company_id):
        with self.__db.connect() as conn:
            result = conn.execute(
                self.__scripts["find_by_id"], {"id": company_id}
            )
            return result.mappings().first()

    def list_companies(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["list_companies"])
            return result.mappings().all()
