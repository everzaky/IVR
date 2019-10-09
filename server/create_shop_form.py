from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, MultipleFileField

class CreateShopForm(FlaskForm):
    name = StringField()
    location = StringField()
    files = MultipleFileField()
    submit = SubmitField()