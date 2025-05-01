from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "<p>You are on login page</p>"

@auth.route("/register")
def register():
    return "<p>You are on register page</p>"

@auth.route("/logout")
def logout():
    return "<p>You are on logout page</p"