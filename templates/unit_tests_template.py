import unittest
from .{{ model_name.lower() }} import {{ model_name }}
from .{{ model_name.lower() }}_repository import {{ model_name }}Repository

class Test{{ model_name }}(unittest.TestCase):
    def setUp(self):
        self.repo = {{ model_name }}Repository(":memory:")
        self.repo.conn.executescript("""
            CREATE TABLE {{ model_name.lower() }} (
                {% for field in fields %}
                {{ field.name }} {{ field.type.upper() }}{% if field.primary_key %} PRIMARY KEY AUTOINCREMENT{% endif %}{% if not loop.last %},{% endif %}
                {% endfor %}
            );
        """)

    def test_create(self):
        {{ model_name.lower() }} = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        id = self.repo.create({{ model_name.lower() }})
        self.assertIsNotNone(id)

    def test_read(self):
        {{ model_name.lower() }} = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        id = self.repo.create({{ model_name.lower() }})
        read_{{ model_name.lower() }} = self.repo.read(id)
        self.assertIsNotNone(read_{{ model_name.lower() }})
        self.assertEqual(read_{{ model_name.lower() }}.id, id)

    def test_update(self):
        {{ model_name.lower() }} = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        id = self.repo.create({{ model_name.lower() }})
        {{ model_name.lower() }}.id = id
        {{ model_name.lower() }}.{{ fields[1].name }} = {{ fields[1].type }}()  # Update the second field
        success = self.repo.update({{ model_name.lower() }})
        self.assertTrue(success)
        updated_{{ model_name.lower() }} = self.repo.read(id)
        self.assertEqual(updated_{{ model_name.lower() }}.{{ fields[1].name }}, {{ model_name.lower() }}.{{ fields[1].name }})

    def test_delete(self):
        {{ model_name.lower() }} = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        id = self.repo.create({{ model_name.lower() }})
        success = self.repo.delete(id)
        self.assertTrue(success)
        deleted_{{ model_name.lower() }} = self.repo.read(id)
        self.assertIsNone(deleted_{{ model_name.lower() }})

    def test_list_all(self):
        {{ model_name.lower() }}1 = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        {{ model_name.lower() }}2 = {{ model_name }}({% for field in fields if not field.primary_key %}{{ field.name }}={{ field.type }}(){% if not loop.last %}, {% endif %}{% endfor %})
        self.repo.create({{ model_name.lower() }}1)
        self.repo.create({{ model_name.lower() }}2)
        {{ model_name.lower() }}s = self.repo.list_all()
        self.assertEqual(len({{ model_name.lower() }}s), 2)

if __name__ == '__main__':
    unittest.main()