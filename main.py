import datetime, os
from dateutil import tz

from flask import Flask,Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login  import current_user
import flask_login
from . import model
from .app import db
from .model import SurveyState, QuestionType

from datetime import datetime as dt

# from sqlalchemy import or_

bp = Blueprint("main", __name__)

@bp.route("/")
@flask_login.login_required
def index():
    surveys = model.Survey.query.filter_by(user_id=current_user.id).order_by(model.Survey.time_created.desc()).limit(10).all()
    return render_template("main/index.html",surveys=surveys)

# @bp.route("/profile/<int:user_id>")
@flask_login.login_required
@bp.route("/account/<int:user_id>")
def profile(user_id):
    # user = model.User.query.filter_by(id=user_id).first_or_404()
    # user_surveys = model.Survey.query.filter_by(user=user).order_by(model.Survey.time_created.desc()).all()
    return redirect(url_for("auth.account"))#,responses=None)

@bp.route("/new_survey",methods=["POST"])
@flask_login.login_required
def create_new_survey():
    questionTypes = [
        model.QuestionType.SELECT,
        model.QuestionType.MULTISELECT,
        model.QuestionType.TEXT,
        model.QuestionType.NUMBER
    ]

    json_data = request.get_json()
    if json_data is not None:
        survey_name = json_data['name']
        timestamp = dt.now(tz.tzlocal())
        state =  model.SurveyState.ONLINE
        newSurvey = model.Survey(
            user=current_user,
            title = survey_name,
            time_created = timestamp,
            state = state
        )
        db.session.add(newSurvey)
        db.session.flush()
        survey_questions = json_data['questions']
        questions = {}
        for i,new_question in enumerate(survey_questions):
            print(new_question)
            question_type = int(new_question['type'])
            question_title = new_question['title']
            question = model.Question(
                survey = newSurvey,
                position = i,
                type = questionTypes[question_type-1],
                title = question_title
            )
            db.session.add(question)
            db.session.flush()
            print(question.id)
            choices = []
            for option in new_question['options']:
                newChoice = model.Choice(
                    question_id = question.id,
                    number=int(option['number']),
                    text=option['text']
                    )
                choices.append(newChoice)
            db.session.add_all(choices)
    db.session.commit()

    return redirect(request.referrer)#url_for("main.index")


@bp.route("/survey/<int:survey_uri>",methods=["POST"])
@flask_login.login_required
def survey(survey_uri):
    survey = model.Survey.query.filter_by(id=survey_uri).first_or_404()
    if survey.state == model.SurveyState.CLOSED:
        print("Survey is closed at the moment.")
        abort(403)

    render_template("templates/survey_response_template.html",survey=survey)


@bp.route("/change_survey_state/<int:survey_id>",methods=["GET","POST"])
@flask_login.login_required
def change_survey_state(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id).first_or_404()
    if survey.user_id != current_user.id:
        print("This user cant change this survey")
        abort(403)

    print("Change state of survey with id:", survey.id)
    if survey.state == model.SurveyState.CLOSED:
        survey.state = model.SurveyState.ONLINE
    else:
        survey.state = model.SurveyState.CLOSED

    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/delete_survey/<int:survey_id>",methods=["GET","POST"])
@flask_login.login_required
def delete_survey(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id).first_or_404()
    if survey.user_id != current_user.id:
        print("This user cant change this survey");
        abort(403)
    print("delete survey with id:", survey.id)
    # model.Survey.query.filter_by(id=survey_id).delete(survey_id)
    db.session.delete(survey)
    db.session.commit()
    return redirect(url_for("main.index"))


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    app.run(env)
