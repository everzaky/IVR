from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class ProducerForm(FlaskForm):
    name = StringField()
    submit = SubmitField()