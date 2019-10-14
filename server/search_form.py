from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, MultipleFileField, IntegerField, TextAreaField

class SearchForm(FlaskForm):
    value = StringField()
    submit = SubmitField()