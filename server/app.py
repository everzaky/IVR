from flask import Flask, render_template, request
from users_model import UsersModel
from db import DB


app = Flask(__name__ )
db = DB()
UsersModel(db.get_connection()).init_table()
app.config['SECRET_KEY'] = 'nothing'


@app.route('/create/<string:user_name>/<string:password>/<string:email>')
def create_user(user_name, password, email):
    um = UsersModel(db.get_connection())
    if um.find_email(email)[0]:
        return "Такая почта уже используется"
    else:
        if um.find(user_name)[0]:
            return "Пользователь с таким именем уже существует"
        else:
            um.insert(user_name=user_name, password=password, email=email, rights="user")
            return "Ok"

@app.route('/enter/<string:user_name>/<string:password>')
def enter_user(user_name, password):
    um = UsersModel(db.get_connection())
    if (um.exists(user_name=user_name, password=password)[0]):
        return "Hello, World!"
    else:
        return "Неправильный логин или пароль"




if __name__ == '__main__':
    app.run(debug=True)
