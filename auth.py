from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from flask_login  import current_user

#Import classes/functions from project modules:
from .app import db, bcrypt
from . import model
from .forms import SignUp, LogIn

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("auth/login.html",form=LogIn())

@bp.route("/login", methods=['POST'])
def login_post():
    form = LogIn()
    email = form.email.data
    password = form.password.data

    # Get the user with the given email from the database:
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # The user exists and the password is correct
        print("USER EXISTS")
        flask_login.login_user(user)
        print(current_user)
        return redirect(url_for("main.index"))
    else:
        # Wrong email and/or password
        flash("Wrong email and/or password!", 'warning')

    return render_template("auth/login.html",form=form)

@bp.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUp()
    email = form.email.data
    username = form.username.data
    password = form.password.data

    if not form.validate_on_submit():
        print("Unvalidated!")
        return render_template("auth/signup.html",form = SignUp())

    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Sorry, passwords are different", 'warning')
        return render_template("auth/signup.html",form=SignUp()) #redirect(url_for("auth.signup"))

    # Check if the email is already at the database
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("Sorry, the email you provided is already registered", 'warning')
        return render_template("auth/signup.html",form=SignUp()) #redirect(url_for("auth.signup"))

    #If none of the above conditions are met then the new user is created:
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash("You've successfully signed up!",'success')
    return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("auth.login"))
