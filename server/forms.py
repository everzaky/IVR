from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SelectField, FileField, PasswordField, MultipleFileField, IntegerField, TextAreaField, BooleanField

class AddFavProduct(FlaskForm):
    submit = SubmitField()
    select1 = SelectField()
    select2 = SelectField()

class CategoryForm(FlaskForm):
    NameCategory = StringField('Имя продуктовой аллеи')
    submit = SubmitField('Добавить')

class CountryForm(FlaskForm):
    name = StringField()
    flag = FileField()
    submit = SubmitField()

class CreateShopForm(FlaskForm):
    name = StringField()
    location = StringField()
    files = FileField()
    submit = SubmitField()

class ForgotForm(FlaskForm):
    email = StringField()
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField()

class ProducerForm(FlaskForm):
    name = StringField()
    submit = SubmitField()

class ProductForm(FlaskForm):
    name = StringField()
    select = SelectField()
    file = MultipleFileField()
    submit = SubmitField()
    price = IntegerField()
    text = TextAreaField()
    producer = SelectField()
    country = SelectField()

class RegistrationForm(FlaskForm):
    login =StringField()
    password = PasswordField()
    email = StringField()
    submit = SubmitField()
    sales_notif = BooleanField()
    sales_notif_fav_products = BooleanField()

class ResetPassword(FlaskForm):
    new_password = PasswordField()
    submit = SubmitField()

class SearchForm(FlaskForm):
    value = StringField()
    submit = SubmitField()