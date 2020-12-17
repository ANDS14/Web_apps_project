from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from flask_login  import current_user,login_required
import secrets, os
from PIL import Image



#Import classes/functions from project modules:
from .app import db, bcrypt
from . import model
from .forms import SignUp, LogIn,UpdateProfile

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=['GET'])
def login():
    form=LogIn()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("auth/login.html",form=form)

@bp.route("/login", methods=['POST'])
def login_post():
    form = LogIn()

    # Get the user with the given email from the database:
    user = model.User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        # The user exists and the password is correct
        print("USER EXISTS")
        flask_login.login_user(user)
        print(current_user)
        return redirect(url_for("main.index"))
    else:
        # Wrong email and/or password
        flash("Wrong email and/or password!", 'danger')

    return render_template("auth/login.html",form=form)

@bp.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUp()

    if form.validate_on_submit():

        user = model.User.query.filter_by(name = form.username.data).first()
        email = model.User.query.filter_by(email = form.email.data).first()

        if  user or email:
            flash("Username or email already taken", 'danger')
            return redirect(url_for("auth.signup"))

        else:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            new_user = model.User(email=form.email.data, name=form.username.data, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash("You've successfully signed up!",'success')
            return redirect(url_for("auth.login"))

    return render_template("auth/signup.html",form=form) #redirect(url_for("auth.signup"))

@bp.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("auth.login"))


def save_image(picture):

    randomize = secrets.token_hex(8)

    name,picture_extension = os.path.splitext(picture.filename)

    new_name = randomize + picture_extension

    new_path = os.path.join(bp.root_path,"static","pics",new_name)

    image_ = Image.open(picture)
    image_.save(new_path)

    return new_name


@bp.route("/account",methods = ['GET','POST'])
@login_required
def account():
    updated_form = UpdateProfile()

    if updated_form.validate_on_submit():
        if current_user.name != updated_form.username.data:
            user = model.User.query.filter_by(name = updated_form.username.data).first()
            if user:
                flash("Username is already taken","danger")
                return redirect(url_for('auth.account'))


        if current_user.email != updated_form.email.data:
            email = model.User.query.filter_by(email = updated_form.email.data).first()
            if email:
                flash("Email is already taken","danger")
                return redirect(url_for('auth.account'))

        current_user.name = updated_form.username.data
        current_user.email = updated_form.email.data

        if updated_form.profile_picture.data:
            new_image = save_image(updated_form.profile_picture.data)
            current_user.profile_image = new_image

        db.session.commit()
        flash("Your account has been updated!", 'success')
        # we redirect here because when we open the browser after submitting we get a message
        # that asks ud whether we want to submit the form again
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        updated_form.username.data = current_user.name
        updated_form.email.data = current_user.email

    image = url_for("static",filename = "/pics/"+ str(current_user.profile_image))
    return render_template('auth/account.html',image = image,form = updated_form)
