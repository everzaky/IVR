from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, DecimalField, PasswordField, BooleanField

class RegistrationForm(FlaskForm):
    login =StringField()
    password = PasswordField()
    email = StringField()
    submit = SubmitField()
    sales_notif = BooleanField()
    sales_notif_fav_products = BooleanField()