from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField

class ProductForm(FlaskForm):
    name = StringField()
    select = SelectField()
    file = FileField()
    submit = SubmitField()