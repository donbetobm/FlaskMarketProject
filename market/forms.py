from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label="User name")
    email_address = StringField(label="E-mail Address")
    password1 = PasswordField(label="Enter Your Password")
    password2 = PasswordField(label="Confirm your Password")
    submit = SubmitField(label="Create Account")
