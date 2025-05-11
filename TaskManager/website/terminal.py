from .db_operations import try_add_new_task
from .models import AddTaskRequestModel, TargetSpecificTaskModel
from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

terminal = Blueprint('terminal', __name__)

@terminal.route('/view', methods=['POST'])
@login_required
def view():
    """Allows to see all contents of one specific task based on its id OR the alias (name) given it by the user"""
    try:
        task_data = TargetSpecificTaskModel.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    return jsonify({"status": "success", "result": "view command has been received"})

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
        return jsonify({"status": "error", "message": result.message}), 400
    msg = (f"Your task '{task_data.title}', with importance {task_data.importance} and deadline {task_data.deadline} "
           f"has been succesfully added.'")
    return jsonify({"status": "success", "result": msg}), 200

@terminal.route('/list', methods=['POST'])
@login_required
def show_list():
    """Shows all tasks of requesting user"""
    # unfortunately name 'list' is built in python
    return jsonify({"status": "success", "result": "list command has been received"})

@terminal.route('/delete', methods=['POST'])
@login_required
def delete():
    """Deletes a task from the database, based on its id OR alias given by the user"""
    try:
        task_data = TargetSpecificTaskModel.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    return jsonify({"status": "success", "result": "del command has been received"})

@terminal.route('/edit', methods=['POST'])
@login_required
def edit():
    """
    Allows user to edit everything in the task (except id). Task to edit can be chosen
    either by its id OR alias given by the user
    """
    try:
        task_data = TargetSpecificTaskModel.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    return jsonify({"status": "success", "result": "edit command has been received"})


