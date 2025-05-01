from flask import Blueprint

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/index")
def index():
    return "<p>You are on the index page</p>"