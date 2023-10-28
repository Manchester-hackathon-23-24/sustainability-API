from flask import Blueprint, request
from utils.db import User, TaskQueue
from utils.constants import TASKS, USERS

from io import BytesIO

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasksqueue/get')
def tasks_queue():
    """Returns the tasks queue"""
    
    # TODO add authorisation

    return [{k, v} for k, v in TaskQueue().cache if k != 'task_info'] # Return pending tasks without image

@tasks.route('/tasksqueue/approve/<task_id>/<user_id>', methods=['POST'])
def tasks_queue_approve(task_id: int, user_id: int):
    """Approves a task"""
    
    # TODO add authorisation

    TaskQueue().approve_task(task_id, user_id)
    return {'status': 'success'}, 200

@tasks.route('/tasksqueue/deny/<task_id>/<user_id>', methods=['POST'])
def tasks_queue_deny(task_id: int, user_id: int):
    """Denies a task"""
    
    # TODO add authorisation

    TaskQueue().deny_task(task_id, user_id)
    return {'status': 'success'}, 200

@tasks.route('/tasksqueue/image/<task_id>/<user_id>', methods=['GET'])
def tasks_queue_image(task_id: int, user_id: int):
    """Returns the image of a task"""
    
    # TODO add authorisation

    return TaskQueue().get_task_image(task_id, user_id), 200

@tasks.route('/tasksqueue/submit/<task_id>/<user_id>', methods=['POST'])
def tasks_queue_submit(task_id: int, user_id: int):
    """Submits a task to the queue"""
    
    # TODO add authorisation

    buffer = BytesIO()
    request.files['image'].save(buffer)

    TaskQueue().add_task(user_id, task_id, buffer)
    return {'status': 'success'}, 200

@tasks.route('/tasks', methods=['GET'])
def tasks_get():
    """Returns all current tasks"""
    
    for task in TASKS:
        if task["type"] == "image":
            task["submitted"] = USERS.count_documents({"completed_task": {"$in": task["id"]}})
        elif task["type"] == "fundraiser":
            # TODO Jason implement fundraisert total money raised for event
            pass

    return TASKS, 200