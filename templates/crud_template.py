import sqlite3
from typing import List, Optional
from .{{ model_name.lower() }} import {{ model_name }}

class {{ model_name }}Repository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self, {{ model_name.lower() }}: {{ model_name }}) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO {{ model_name.lower() }} ({% for field in fields if not field.primary_key %}{{ field.name }}{% if not loop.last %}, {% endif %}{% endfor %})
                VALUES ({% for field in fields if not field.primary_key %}:{{ field.name }}{% if not loop.last %}, {% endif %}{% endfor %})
            """, {{ model_name.lower() }}.to_dict())
            return cursor.lastrowid

    def read(self, id: int) -> Optional[{{ model_name }}]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM {{ model_name.lower() }} WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return {{ model_name }}.from_dict(dict(zip([column[0] for column in cursor.description], row)))
            return None

    def update(self, {{ model_name.lower() }}: {{ model_name }}) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE {{ model_name.lower() }}
                SET {% for field in fields if not field.primary_key %}{{ field.name }} = :{{ field.name }}{% if not loop.last %}, {% endif %}{% endfor %}
                WHERE id = :id
            """, {{ model_name.lower() }}.to_dict())
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM {{ model_name.lower() }} WHERE id = ?", (id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[{{ model_name }}]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM {{ model_name.lower() }}")
            return [{{ model_name }}.from_dict(dict(zip([column[0] for column in cursor.description], row))) for row in cursor.fetchall()]