from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class ResetPassword(FlaskForm):
    new_password = PasswordField()
    submit = SubmitField()