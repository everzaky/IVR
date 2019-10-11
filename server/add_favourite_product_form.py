from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SelectField

class AddFavProduct(FlaskForm):
    submit = SubmitField()
    select1 = SelectField()
    select2 = SelectField()