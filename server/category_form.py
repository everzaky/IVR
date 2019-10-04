from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField

class CategoryForm(FlaskForm):
    NameCategory = StringField('Имя продуктовой аллеи')
    submit = SubmitField('Добавить')