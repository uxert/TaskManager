from flask import Blueprint, jsonify
from flask_login import login_required



terminal = Blueprint('terminal', __name__)

@terminal.route('/view', methods=['POST'])
@login_required
def view():
    return jsonify({"status": "success", "result": "view command has been received"})

@terminal.route('/add', methods=['POST'])
@login_required
def add():
    return jsonify({"status": "success", "result": "add command has been received"})

@terminal.route('/list', methods=['POST'])
@login_required
def show_list():
    # unfortunately name 'list' is built in python
    return jsonify({"status": "success", "result": "list command has been received"})

@terminal.route('/delete', methods=['POST'])
@login_required
def delete():
    return jsonify({"status": "success", "result": "del command has been received"})

@terminal.route('/edit', methods=['POST'])
@login_required
def edit():
    return jsonify({"status": "success", "result": "edit command has been received"})


