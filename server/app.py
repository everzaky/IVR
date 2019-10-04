from flask import Flask, render_template, request
from users_model import UsersModel
from db import DB
from category_form import CategoryForm
from category_model import CategoryModel
from product_form import ProductForm
import os


app = Flask(__name__ )
db = DB()
UsersModel(db.get_connection()).init_table()
CategoryModel(db.get_connection()).init_table()
app.config['SECRET_KEY'] = 'nothing'
app.config['UPLOAD_FOLDER']="D:\\E1\\IVR\\server\\static\\img"


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

@app.route('/create_category', methods=["GET", "POST"])
def create_category():
    CF = CategoryForm()
    CM = CategoryModel(db.get_connection())
    if (request.method=="POST"):
        name_category = CF.NameCategory.data
        if (CM.exists(name_category)):
            return render_template('category.html', args=["Exists"], form = CF)
        else:
            CM.insert(name_category,"")
            return render_template('category.html', args=["Done"], form = CF)

    else:
        return render_template('category.html', args=["kek"], form = CF)



@app.route('/create_product', methods=["GET", "POST"])
def create_product():
    CM = CategoryModel(db.get_connection())
    categories = CM.get_all()
    choises = [i[1] for i in categories]
    Pf = ProductForm()
    Pf.select.choices=choises
    if request.method=="POST":
        img = Pf.file.data
        rash = img.filename.split(".")
        img.filename = Pf.name.data+"."+rash[1]
        img.save(os.path.join(app.config["UPLOAD_FOLDER"], img.filename))
    return render_template("product.html", form = Pf)


if __name__ == '__main__':
    app.run(debug=True)
