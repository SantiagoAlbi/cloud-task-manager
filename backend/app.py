from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir requests desde frontend

# Base de datos en memoria por ahora (después migraremos a MySQL)
tasks = []
next_id = 1

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas"""
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    """Crear nueva tarea"""
    global next_id
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = {
        "id": next_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    tasks.append(task)
    next_id += 1
    
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtener tarea específica"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualizar tarea"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar tarea"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
