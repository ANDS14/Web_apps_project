from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from flask_login  import current_user
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
def logout():
    flask_login.logout_user()
    return redirect(url_for("auth.login"))


def save_pic(pic_name):
    # we do not want to keep the name of the uploaded file because it could collide
    # with an existing file in our pics folder.
    # Therefore, we randomized it.
    random_hex = secrets.token_hex(8)

    # Upload the new picture with the same file extension
    _ , f_extension =  os.path.splitext(pic_name.filename)

    new_image = random_hex + f_extension

    # Suppose that we upload a large file. CSS will resize it to 125x125 and update with thta image the profile picture.
    # In order to optimize the performance, we previously resize to 125x125 using the Pillow module
    size = (125,125)
    image_resize = Image.open(pic_name)
    image_resize.thumbnail(size)

    pic_path = os.path.join(bp.root_path,'BurritoSurvey/static/pics',new_image)
    image_resize.save(pic_path) # Image saved but not in the database

    return new_image


@bp.route("/account",methods = ['GET','POST'])
def account():
    updated_form = UpdateProfile()

    if updated_form.validate_on_submit():

        #if updated_form.picture.data:
            #pic_file = save_pic(updated_form.picture.data)
            #current_user.profile_image = pic_file

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
        db.session.commit()

        flash("Your account has been updated!", 'success')

        # we redirect here because when we open the browser after submitting we get a message
        # that asks ud whether we want to submit the form again
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        updated_form.username.data = current_user.name
        updated_form.email.data = current_user.email

    #image = url_for('static',filename ="pics/"+current_user.profile_image)
    return render_template('auth/account.html',form = updated_form)
