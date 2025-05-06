from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


WEBSITE_DIR = path.dirname(path.abspath(__file__))
BACKEND_DIR = path.dirname(WEBSITE_DIR)

db = SQLAlchemy()
DATABASE_NAME = "database.db"
DATABASE_PATH = path.join(BACKEND_DIR, DATABASE_NAME)
TEST_DATABASE_PATH = path.join(BACKEND_DIR, "test.db")

def create_app(test=False):
    from .views import views
    from .auth import auth
    from .terminal import terminal

    database_path = TEST_DATABASE_PATH if test else DATABASE_PATH
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "<KEY>"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    db.init_app(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(terminal, url_prefix="/terminal")

    from .models import User, Task  # so that these classes are actually  defined when creating the database
    create_database(app, database_path)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app: Flask, database_path):
    if not path.exists(database_path):
        with app.app_context():
            db.create_all()
        print(f"Created database at {database_path}!")