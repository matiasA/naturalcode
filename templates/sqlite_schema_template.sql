CREATE TABLE IF NOT EXISTS {{ model_name.lower() }} (
    {% for field in fields %}
    {{ field.name }} {{ field.type.upper() }}{% if field.primary_key %} PRIMARY KEY AUTOINCREMENT{% endif %}{% if not loop.last %},{% endif %}
    {% endfor %}
);