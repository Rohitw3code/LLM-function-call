from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    # Initialize the SQLite database and create the tasks table if it doesn't exist
    with sqlite3.connect("todo.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending'
        )
        """)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add_task():
    """Add a new task."""
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    
    if not title:
        return jsonify({"error": "Title is required."}), 400

    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
        conn.commit()
        task_id = cursor.lastrowid

    return jsonify({"id": task_id, "title": title, "description": description, "status": "pending"}), 201

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    data = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')

    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            return jsonify({"error": "Task not found."}), 404

        cursor.execute("""
        UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?
        """, (title or task[1], description or task[2], status or task[3], task_id))
        conn.commit()

    return jsonify({"message": "Task updated successfully."})

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            return jsonify({"error": "Task not found."}), 404

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

    return jsonify({"message": "Task deleted successfully."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)