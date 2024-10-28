from flask import Blueprint, jsonify, request
from db import fetch_all_tasks, add_task_to_db, mark_task_complete, delete_task_from_db, fetch_sorted_tasks, search_tasks

tasks_bp = Blueprint('tasks', __name__)

# Get all tasks
@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = fetch_all_tasks()
    task_list = [dict(task) for task in tasks]
    return jsonify(task_list)

# Add new task
@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    title = task_data.get('title')
    description = task_data.get('description')
    due_date = task_data.get('due_date')
    priority = task_data.get('priority')

    add_task_to_db(title, description, due_date, priority)
    return jsonify({'message': 'Task added successfully!'})

# Mark task as complete
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    mark_task_complete(task_id)
    return jsonify({'message': 'Task marked as completed!'}), 200

# Delete a task
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    delete_task_from_db(task_id)
    return jsonify({'message': 'Task deleted!'}), 200

# Sort tasks by priority or due date
@tasks_bp.route('/tasks/sorted', methods=['GET'])
def get_sorted_tasks():
    sort_by = request.args.get('sort_by', 'priority')  # Default to sorting by priority
    sorted_tasks = fetch_sorted_tasks(sort_by)
    task_list = [dict(task) for task in sorted_tasks]
    return jsonify(task_list)

@tasks_bp.route('/tasks/search', methods=['GET'])
def search_route():
    search_query = request.args.get('query', '')
    found_tasks = search_tasks(search_query) if search_query else []
    task_list = [dict(task) for task in found_tasks]
    return jsonify(task_list)