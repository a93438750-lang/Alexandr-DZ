from sqlalchemy import create_engine, text

class CompanyTable:
    __scripts = {
        "insert": text("INSERT INTO company (name, description) VALUES (:name, :description) RETURNING id"),
        "update": text("UPDATE company SET name=:new_name, description=:new_description WHERE id=:id"),
        "delete": text("UPDATE company SET deleted_at=NOW() WHERE id=:id"),  # Мягкое удаление
        "find_by_id": text("SELECT * FROM company WHERE id=:id AND deleted_at IS NULL"),
        "list_companies": text("SELECT * FROM company WHERE deleted_at IS NULL")
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def add_company(self, name, description):
        conn = self.__db.connect()
        result = conn.execute(self.__scripts["insert"], {"name": name, "description": description})
        new_id = result.scalar_one()
        conn.close()
        return new_id

    def update_company(self, company_id, new_name, new_description):
        conn = self.__db.connect()
        conn.execute(self.__scripts["update"], {"id": company_id, "new_name": new_name, "new_description": new_description})
        conn.commit()
        conn.close()

    def delete_company(self, company_id):
        conn = self.__db.connect()
        conn.execute(self.__scripts["delete"], {"id": company_id})
        conn.commit()
        conn.close()

    def get_company_by_id(self, company_id):
        conn = self.__db.connect()
        result = conn.execute(self.__scripts["find_by_id"], {"id": company_id})
        row = result.mappings().first()
        conn.close()
        return row

    def list_companies(self):
        conn = self.__db.connect()
        result = conn.execute(self.__scripts["list_companies"])
        rows = result.mappings().all()
        conn.close()
        return rows