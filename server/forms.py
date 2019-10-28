from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SelectField, FileField, PasswordField, MultipleFileField, IntegerField, TextAreaField, BooleanField, DecimalField, FloatField
from wtforms.validators import  DataRequired

class ChooseProduct(FlaskForm):
    submit = SubmitField()
    select1 = SelectField()
    select2 = SelectField()

class CategoryForm(FlaskForm):
    NameCategory = StringField('Имя продуктовой аллеи')
    submit = SubmitField('Добавить')

class RecreateCategoryForm(FlaskForm):
    NameCategory = StringField()
    submit = SubmitField()

class CountryForm(FlaskForm):
    name = StringField()
    flag = FileField()
    submit = SubmitField()

class RecreateCountryForm(FlaskForm):
    name = StringField()
    flag = FileField()
    submit = SubmitField()

class CreateShopForm(FlaskForm):
    name = StringField()
    location = StringField()
    files = MultipleFileField()
    submit = SubmitField()

class ForgotForm(FlaskForm):
    email = StringField()
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField(DataRequired())
    password = PasswordField(DataRequired())
    submit = SubmitField()

class ProducerForm(FlaskForm):
    name = StringField()
    submit = SubmitField()

class ProductForm(FlaskForm):
    name = StringField()
    select = SelectField()
    file = MultipleFileField()
    submit = SubmitField()
    price = FloatField()
    text = TextAreaField()
    producer = SelectField()
    country = SelectField()

class RegistrationForm(FlaskForm):
    login =StringField(DataRequired())
    password = PasswordField(DataRequired())
    email = StringField(DataRequired())
    submit = SubmitField()
    sales_notif = BooleanField()
    sales_notif_fav_products = BooleanField()

class ResetPassword(FlaskForm):
    new_password = PasswordField()
    submit = SubmitField()

class SearchForm(FlaskForm):
    value = StringField()
    submit = SubmitField()

class PosProduct(FlaskForm):
    number=IntegerField()
    output = StringField()
    submit = SubmitField()
    price = FloatField()