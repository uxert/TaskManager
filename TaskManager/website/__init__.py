from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

WEBSITE_DIR = path.dirname(path.abspath(__file__))
BACKEND_DIR = path.dirname(WEBSITE_DIR)

db = SQLAlchemy()
DATABASE_NAME = "database.db"
DATABASE_PATH = path.join(BACKEND_DIR, DATABASE_NAME)

def create_app():
    from .views import views
    from .auth import auth

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "<KEY>"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
    db.init_app(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Task  # so that these classes are actually  defined when creating the database
    create_database(app)

    return app

def create_database(app: Flask):
    if not path.exists(DATABASE_PATH):
        with app.app_context():
            db.create_all()
        print(f"Created database at {DATABASE_PATH}!")