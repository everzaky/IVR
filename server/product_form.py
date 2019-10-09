from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, MultipleFileField, IntegerField

class ProductForm(FlaskForm):
    name = StringField()
    select = SelectField()
    file = MultipleFileField()
    submit = SubmitField()
    price = IntegerField()