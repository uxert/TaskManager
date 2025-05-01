from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/index")
def index():
    return render_template("home.html")

@views.route("/terminal")
def terminal():
    return render_template("terminal.html")