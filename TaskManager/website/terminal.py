from flask import Blueprint, jsonify, request
from flask_login import login_required
from .models import AddTaskRequestModel, TargetSpecificTaskModel
from pydantic import ValidationError


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
    return jsonify({"status": "success", "result": "add command has been received"})

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


