from flask import Flask, jsonify, request

# Inicializace Flask aplikace
app = Flask(__name__)

# Úkoly jsou uloženy v paměti
tasks = []

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Vrací seznam všech úkolů."""
    return jsonify(tasks), 200

@app.route("/tasks", methods=["POST"])
def add_task():
    """Přidává nový úkol."""
    data = request.json
    if "description" in data:
        task = {
            "id": len(tasks) + 1,
            "description": data["description"],
            "assigned_to": None,
            "completed": False
        }
        tasks.append(task)
        return jsonify(task), 201
    return jsonify({"error": "Invalid data"}), 400

@app.route("/tasks/<int:task_id>/assign", methods=["PUT"])
def assign_task(task_id):
    """Přiřazuje úkol uživateli."""
    data = request.json
    for task in tasks:
        if task["id"] == task_id:
            task["assigned_to"] = data.get("user", None)
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    """Označuje úkol jako dokončený."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

def run_flask():
    """Spuštění Flask serveru."""
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
