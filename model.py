#DEFINES THE SCHEMA OF OUR APPLICATION'S DATABASE
from .app import db
import flask_login
from flask_login  import current_user

import enum

class User(flask_login.UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.String(20),nullable=False,default = "user_icon.png")
    surveys = db.relationship('Survey', backref='user', lazy=True,cascade="all, delete-orphan",)

class SurveyState(enum.Enum):
    NEW = 1
    ONLINE = 2
    CLOSED = 3

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    questions = db.relationship(
        "Question",
        backref="survey",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Question.position",
    )
    state = db.Column(db.Enum(SurveyState), nullable=False)
    time_created = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Float, nullable=True,default=0)

class QuestionType(enum.Enum):
    SELECT = 1
    MULTISELECT = 2
    TEXT = 3
    NUMBER = 4
    POLL = 5

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("survey.id"), nullable=False)
    position = db.Column(db.Integer, autoincrement=True)
    type = db.Column(db.Enum(QuestionType), nullable=False)

class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(), nullable=False)

    selected = db.Column(db.Integer)
    text = db.Column(db.String(512))
    number = db.Column(db.Integer)
