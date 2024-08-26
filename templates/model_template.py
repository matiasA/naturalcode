class {{ model_name }}:
    def __init__(self{% for field in fields %}, {{ field.name }}: {{ field.type }}{% endfor %}):
        {% for field in fields %}
        self.{{ field.name }} = {{ field.name }}
        {% endfor %}

    def to_dict(self):
        return {
            {% for field in fields %}
            "{{ field.name }}": self.{{ field.name }},
            {% endfor %}
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            {% for field in fields %}
            {{ field.name }}=data["{{ field.name }}"],
            {% endfor %}
        )