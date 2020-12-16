'''

Classes used for html form handling using Flask-wtf.

flask_wtf is a flask module that handles passing data from html forms.

We use flask-wtf in our project to validate the forms used for user authentication and
the creation of surveys.

Documentation of the module:
https://flask-wtf.readthedocs.io/en/stable/form.html
'''

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField,SubmitField,validators
from flask_wtf.file import FileAllowed, FileField


class SignUp(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=2, max=12)])

    email = StringField('Email Address', [validators.DataRequired(),validators.Email()])

    password = PasswordField('Password', [validators.DataRequired()])

    password_confirm = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password')])

    submit = SubmitField('Sign Up')

class LogIn(FlaskForm):

    email = StringField('Email Address', [validators.DataRequired(),validators.Email()])

    password = PasswordField('Password', [validators.DataRequired()])

    submit = SubmitField('Log In')


class UpdateProfile(FlaskForm):

    username = StringField('Username', [validators.DataRequired(),validators.Length(min=2, max=12)])

    email = StringField('Email Address', [validators.DataRequired(),validators.Email()])

    profile_picture = FileField("Profile picture", validators = [FileAllowed(['png'])])

    submit = SubmitField('Update')
