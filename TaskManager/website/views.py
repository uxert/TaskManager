from flask import Blueprint, render_template
from flask_login import login_required


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/index")
@login_required
def index():
    return render_template("home.html")

@views.route("/terminal")
@login_required
def terminal():
    return render_template("terminal.html")