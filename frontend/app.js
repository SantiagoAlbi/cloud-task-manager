const API_URL = 'http://127.0.0.1:5000';

// Cargar tareas al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

// Obtener todas las tareas
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        alert('Error al cargar las tareas');
    }
}

// Mostrar tareas en el DOM
function displayTasks(tasks) {
    const tasksList = document.getElementById('tasksList');
    
    if (tasks.length === 0) {
        tasksList.innerHTML = '<p style="text-align:center; color:#999;">No hay tareas todavía</p>';
        return;
    }
    
    tasksList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <div class="task-content">
                <div class="task-title ${task.completed ? 'completed' : ''}">${task.title}</div>
                ${task.description ? `<div class="task-desc">${task.description}</div>` : ''}
            </div>
            <div class="task-actions">
                ${!task.completed ? 
                    `<button class="btn-complete" onclick="toggleTask(${task.id}, true)">✓ Completar</button>` :
                    `<button class="btn-complete" onclick="toggleTask(${task.id}, false)">↺ Reabrir</button>`
                }
                <button class="btn-delete" onclick="deleteTask(${task.id})">🗑 Eliminar</button>
            </div>
        </div>
    `).join('');
}

// Crear nueva tarea
async function createTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDesc').value.trim();
    
    if (!title) {
        alert('El título es obligatorio');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description })
        });
        
        if (response.ok) {
            document.getElementById('taskTitle').value = '';
            document.getElementById('taskDesc').value = '';
            loadTasks();
        }
    } catch (error) {
        console.error('Error creating task:', error);
        alert('Error al crear la tarea');
    }
}

// Marcar tarea como completada/incompleta
async function toggleTask(id, completed) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed })
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Error al actualizar la tarea');
    }
}

// Eliminar tarea
async function deleteTask(id) {
    if (!confirm('¿Seguro que querés eliminar esta tarea?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Error al eliminar la tarea');
    }
}
