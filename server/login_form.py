from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField()