from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import boto3
import pymysql
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ─── Credenciales desde Secrets Manager ──────────────────────────────────────
def get_db_credentials():
    secret_name = os.getenv("DB_SECRET_NAME", "task-manager/db-credentials")
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def get_db_connection():
    creds = get_db_credentials()
    return pymysql.connect(
        host=creds["host"],
        user=creds["username"],
        password=creds["password"],
        database=creds["dbname"],
        port=int(creds["port"]),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


# ─── Init DB: crea la tabla si no existe ─────────────────────────────────────
def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
    conn.close()


# ─── Endpoints ───────────────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "storage": "mysql", "timestamp": datetime.now().isoformat()}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s)",
            (data['title'], data.get('description', ''), data.get('completed', False)),
        )
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
    conn.close()
    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
    conn.close()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE tasks SET title=%s, description=%s, completed=%s WHERE id=%s",
            (
                data.get('title', task['title']),
                data.get('description', task['description']),
                data.get('completed', task['completed']),
                task_id,
            ),
        )
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated = cursor.fetchone()
    conn.close()
    return jsonify(updated), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        affected = cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.close()
    if affected == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
