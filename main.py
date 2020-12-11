import datetime, os
from dateutil import tz

from flask import Flask,Blueprint, request, render_template, redirect, url_for, flash
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
    other_surveys = model.Survey.query.filter_by(user_id=2).order_by(model.Survey.time_created.desc()).limit(3).all()

    return render_template("main/index.html",surveys=surveys,other_surveys=other_surveys)

#@bp.route("/profile/<int:user_id>")
#@flask_login.login_required
@bp.route("/profile/<int:user_id>")
def profile(user_id):
    user = model.User.query.filter_by(id=user_id).first_or_404()
    user_surveys = model.Survey.query.filter_by(user=user).order_by(model.Survey.time_created.desc()).all()
    return render_template("main/profile.html", user=user,surveys=user_surveys)#,responses=None)

@bp.route("/new_survey",methods=["POST"])
@flask_login.login_required
def create_new_survey():
    # post_text = request.form.get("post_text")
    # response_to = request.form.get("response_to")
    #
    # if response_to is not None:
    #     response_to = model.Message.query.filter_by(id=response_to).first_or_404()
    #
    # if len(post_text)>240:
    #     flash("The text was too long!")
    #     return redirect(url_for("main.index"))
    # print(post_text)
    # post_timestamp = dt.now(dateutil.tz.tzlocal())
    # user = current_user
    # msg = model.Message(
    #     user=user,
    #     text=post_text,
    #     timestamp=post_timestamp,
    #     response_to=response_to
    # )
    # print(msg.user.name)
    # db.session.add(msg)
    # db.session.commit()
    return redirect(url_for("main.index"))#redirect(url_for("main.post",message_id=msg.id))



if __name__ == "__main__":
    from app import create_app
    app = create_app()
    app.run(env)
