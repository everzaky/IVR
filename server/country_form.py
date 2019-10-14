from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class CountryForm(FlaskForm):
    name = StringField()
    flag = FileField()
    submit = SubmitField()