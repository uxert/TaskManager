from flask import Blueprint, render_template, request, flash
from typing import NamedTuple


class SimpleResponse(NamedTuple):
    """ Simple NamedTuple that will allow to pass results from database functions - status and error explanation"""
    success: bool
    message: str = ''

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]



def validate_signup(email, username, password1, password2) -> bool:
    success = True
    if password1 != password2:
        flash("Passwords don't match!", category="error")
        success = False
    if len(username) <= 3:
        flash("Username too short! Should be at least 4 characters", category="error")
        success = False
    if len(password1) <=7: #passwords are equal at this point
        flash("Password too short! Should be at least 8 characters", category="error")
        success = False
    # check if either email or username already used
    if False:
        flash(f"Username {username} is already taken!", category="error")
        success = False
    if False:
        flash(f"Account registered on {email} already exists!", category="error")
        success = False
    return success

def register_user(email, username, password) -> SimpleResponse:
    """Function to register a new user in the database."""
    return SimpleResponse(True)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    email = request.form["email"]
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if validate_signup(email, username, password1, password2) is False:
        return render_template("register.html")

    result = register_user(email, username, password1)
    if result.success is True:
        flash("Account registered successfully!", category="success")
    if result.success is not True:
        flash(f"Account was not registered: {result.message}", category="error")
    return render_template("register.html")

@auth.route("/logout")
def logout():
    return render_template("after_logout.html")