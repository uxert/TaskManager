"""Models for database"""
from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    tasks = db.relationship("Task")

    def __init__(self, email, username, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.email = email
        self.username = username
        self.set_password(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="scrypt")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    est_time_days = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    parent_task_id = db.Column(db.ForeignKey("task.id"), nullable=True)
    children = db.relationship(
        "Task",
        backref=db.backref("parent", remote_side=[id]),
        lazy="select"
    )

    def __init__(self, title, importance, deadline, est_time_days, description, user_id, parent_task_id):
        self.title = title
        self.importance = importance
        self.deadline = deadline
        self.est_time_days = est_time_days
        self.description = description
        self.user_id = user_id
        self.parent_task_id = parent_task_id