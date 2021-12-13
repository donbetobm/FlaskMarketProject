from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label="User name", validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label="E-mail Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Enter Your Password", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm your Password", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")
