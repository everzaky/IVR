from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, FileField

class CreateShopForm(FlaskForm):
    name = StringField()
    location = StringField()
    files = FileField()
    submit = SubmitField()