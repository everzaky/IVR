from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class ForgotForm(FlaskForm):
    email = StringField()
    submit = SubmitField()