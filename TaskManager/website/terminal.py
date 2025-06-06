from .db_operations import try_add_new_task, try_getting_user_tasks, try_getting_specific_task, \
    try_removing_specific_task, try_editing_specific_task
from .models import AddTaskRequestModel, EditTaskRequestModel
from .utils import DateTimeEncoder
from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound
import json


terminal = Blueprint('terminal', __name__)

@terminal.route('/view', methods=['POST'])
@login_required
def view():
    """Allows to see all contents of one specific task based on its id"""
    if not request.json["task_id"].isdigit():
        return jsonify({"status": "error", "message": "Expected task_id to be integer!"}), 400
    task_id = int(request.json["task_id"])
    result = try_getting_specific_task(current_user.id, task_id)
    if result.success is False:
        if isinstance(result.exception, NoResultFound):
            return jsonify({"status": "error", "message": result.message}), 404
        return jsonify({"status": "error", "message": result.message}), 500

    task_dict = result.task
    task_dict.pop("parent_task_id")
    task_dict.pop("user_id")
    return jsonify({"status": "success", "result": json.dumps(task_dict, cls=DateTimeEncoder, indent=4)}), 200

@terminal.route('/add', methods=['POST'])
@login_required
def add():
    """Allows to add a task to the database"""
    try:
        task_data = AddTaskRequestModel.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    user_id = current_user.id
    result = try_add_new_task(task_data, user_id)
    if result.success is False:
        return jsonify({"status": "error", "message": result.message}), 500
    msg = (f"Your task '{task_data.title}', with importance {task_data.importance} and deadline {task_data.deadline} "
           f"has been succesfully added.'")
    return jsonify({"status": "success", "result": msg}), 200

@terminal.route('/list', methods=['POST'])
@login_required
def show_list():
    """Shows all tasks of requesting user"""
    # unfortunately name 'list' is built in python
    result = try_getting_user_tasks(current_user.id)
    if result.success is False:
        if isinstance(result.exception, NoResultFound):
            return jsonify({"status": "error", "message": result.message}), 404
        return jsonify({"status": "error", "message": result.message}), 500
    tasks = result.tasks
    for task in tasks:
        # task.pop("task_id")
        task.pop("parent_task_id")
        task.pop("user_id")
    tasks_json = json.dumps(tasks, indent=4, cls=DateTimeEncoder)
    return jsonify({"status": "success", "result": tasks_json}), 200

@terminal.route('/delete', methods=['POST'])
@login_required
def delete():
    """Deletes a task from the database, based on its id"""
    print(request.json["task_id"])
    if not request.json["task_id"].isdigit():
        return jsonify({"status": "error", "message": "Expected task_id to be integer!"}), 400
    task_id = int(request.json["task_id"])

    result = try_removing_specific_task(current_user.id, task_id)
    if result.success is False:
        if isinstance(result.exception, NoResultFound):
            return jsonify({"status": "error", "message": result.message}), 404
        return jsonify({"status": "error", "message": result.message}), 500

    return jsonify({"status": "success", "result": f"Succesfully deleted task '{result.message}'"}), 200

@terminal.route('/edit', methods=['POST'])
@login_required
def edit():
    """
    Allows user to edit everything in the task (except id). Task to edit can be chosen by its id.
    """
    try:
        edit_request = EditTaskRequestModel.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    user_id = current_user.id
    result = try_editing_specific_task(user_id, edit_request)
    if result.success is False:
        if isinstance(result.exception, NoResultFound):
            return jsonify({"status": "error", "message": result.message}), 404
        return jsonify({"status": "error", "message": result.message}), 500

    return jsonify({"status": "success", "result": result.message}), 200


