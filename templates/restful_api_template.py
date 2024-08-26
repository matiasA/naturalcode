from flask import Flask, request, jsonify
from .{{ model_name.lower() }} import {{ model_name }}
from .{{ model_name.lower() }}_repository import {{ model_name }}Repository

app = Flask(__name__)
repo = {{ model_name }}Repository("database.db")

@app.route("/{{ model_name.lower() }}", methods=["POST"])
def create_{{ model_name.lower() }}():
    data = request.json
    {{ model_name.lower() }} = {{ model_name }}(**data)
    id = repo.create({{ model_name.lower() }})
    return jsonify({"id": id}), 201

@app.route("/{{ model_name.lower() }}/<int:id>", methods=["GET"])
def read_{{ model_name.lower() }}(id):
    {{ model_name.lower() }} = repo.read(id)
    if {{ model_name.lower() }}:
        return jsonify({{ model_name.lower() }}.to_dict())
    return jsonify({"error": "{{ model_name }} not found"}), 404

@app.route("/{{ model_name.lower() }}/<int:id>", methods=["PUT"])
def update_{{ model_name.lower() }}(id):
    data = request.json
    {{ model_name.lower() }} = {{ model_name }}(id=id, **data)
    success = repo.update({{ model_name.lower() }})
    if success:
        return jsonify({{ model_name.lower() }}.to_dict())
    return jsonify({"error": "{{ model_name }} not found"}), 404

@app.route("/{{ model_name.lower() }}/<int:id>", methods=["DELETE"])
def delete_{{ model_name.lower() }}(id):
    success = repo.delete(id)
    if success:
        return "", 204
    return jsonify({"error": "{{ model_name }} not found"}), 404

@app.route("/{{ model_name.lower() }}", methods=["GET"])
def list_{{ model_name.lower() }}s():
    {{ model_name.lower() }}s = repo.list_all()
    return jsonify([{{ model_name.lower() }}.to_dict() for {{ model_name.lower() }} in {{ model_name.lower() }}s])

if __name__ == "__main__":
    app.run(debug=True)