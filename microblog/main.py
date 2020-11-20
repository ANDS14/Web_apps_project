import datetime
import dateutil.tz

from flask import Flask,Blueprint, request, render_template, redirect, url_for, flash
from flask_login  import current_user

import flask_login

from . import model, db

from datetime import datetime as dt

app = Flask(__name__)
bp = Blueprint("main", __name__)

@bp.route("/")
@flask_login.login_required
def index():
    messages = model.Message.query.filter_by(response_to=None).order_by(model.Message.timestamp.desc()).limit(10).all()
    return render_template("main/index.html", posts=messages,responses=None)

@bp.route("/post/<int:message_id>")
@bp.route('/post/<int:message_id>/<int:is_response>')
@flask_login.login_required
def post(message_id,is_response=0):
    message = model.Message.query.filter_by(id=message_id).first_or_404()
    print(message)
    responses = model.Message.query.filter(model.Message.response_to is not None).all()#filter(model.Message.response_to==message_id).order_by(model.Message.timestamp.desc()).all()
    responses = [response for response in responses if response.response_to is not None]
    responses = [response for response in responses if response.response_to.id==message_id]

    return render_template("main/post.html",posts=[message],with_response=bool(is_response),responses=responses)

@bp.route("/new_post",methods=["POST"])
@flask_login.login_required
def create_new_post():
    post_text = request.form.get("post_text")
    response_to = request.form.get("response_to")

    if response_to is not None:
        response_to = model.Message.query.filter_by(id=response_to).first_or_404()

    if len(post_text)>240:
        flash("The text was too long!")
        return redirect(url_for("main.index"))
    print(post_text)
    post_timestamp = dt.now(dateutil.tz.tzlocal())
    user = current_user
    msg = model.Message(
        user=user,
        text=post_text,
        timestamp=post_timestamp,
        response_to=response_to
    )
    print(msg.user.name)
    db.session.add(msg)
    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/profile/<int:user_id>")
@flask_login.login_required
def profile(user_id):
    user = model.User.query.filter_by(id=user_id).first_or_404()
    user_messages = model.Message.query.filter_by(user=user).order_by(model.Message.timestamp.desc()).all()
    return render_template("main/profile.html", user=user,posts=user_messages)
