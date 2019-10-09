from flask import Flask, render_template, request, session
from users_model import UsersModel
from db import DB
from category_form import CategoryForm
from category_model import CategoryModel
from product_form import ProductForm
from product_model import ProductModel
from registration_form import RegistrationForm
from forgot_form import ForgotForm
from login_form import LoginForm
from create_shop_form import CreateShopForm
from shop_model import ShopModel
from shop_db import DB_SHOP
from reset_password_form import ResetPassword
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import datetime


app = Flask(__name__ , static_folder="D:\E1\IVR\server\static")
db = DB()

UsersModel(db.get_connection()).init_table()
CategoryModel(db.get_connection()).init_table()
ProductModel(db.get_connection()).init_table()
ShopModel(db.get_connection()).init_table()
app.config['SECRET_KEY'] = 'nothing'
app.config['UPLOAD_FOLDER']="D:\\E1\\IVR\\server\\static\\img"

#smtpObj.login('pauchan.mobile@mail.ru', 'YS8-pY8-ZZr-JSG')
print("fff")

@app.route("/")
def index():
    return render_template("index.html", session=session)

'''@app.route('/create/<string:user_name>/<string:password>/<string:email>')
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
'''
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
    pm = ProductModel(db.get_connection())
    args = []
    if request.method=="POST":
        if (pm.exists(Pf.name.data)[0]):
            args+=["Exists"]

        else:
            print("kek")
            images=""
            i = 1
            for img in Pf.file.data:
                trash = img.filename.split(".")
                img.filename = Pf.name.data+"_"+str(i)+"."+trash[1]
                print(img.filename)
                i+=1
                images+=img.filename+" "
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], img.filename))
            pm.insert(Pf.name.data, Pf.price.data, 0, False, str(datetime.datetime.now()), str(datetime.datetime.now()),
                      images)
            args+=["OK"]
    return render_template("product.html", form = Pf, args = args)

@app.route('/create_shop', methods = ["GET", "POST"])
def create_shop():
    csf = CreateShopForm()
    sm = ShopModel(db.get_connection())
    args = []
    if (request.method=="POST"):
        if (sm.exists(csf.name.data)[0]):
            args+=["name_exists"]
        else:
            os.makedirs(os.getcwd()+"\\shops\\"+csf.name.data)
            os.makedirs(os.getcwd()+"\\shops\\"+csf.name.data+"\\"+"img")
    return render_template('new_shop.html', args=args, form = csf)

@app.route('/register', methods=["GET", "POST"])
def register():
    lf = RegistrationForm()
    args=[]
    um = UsersModel(db.get_connection())
    if (request.method=="POST"):
        args+=["post"]
        if (um.find(lf.login.data)[0]):
            args+=["exists"]
        if (um.find_email(lf.email.data)[0]):
            args+=['email_exists']
        if ("exists" not in args and "email_exists" not in args):
            print(lf.email.data)
            um.insert(lf.login.data, lf.email.data, lf.password.data, "user", '', lf.sales_notif.data, lf.sales_notif_fav_products.data)

            os.makedirs(os.getcwd()+"\\"+"users"+"\\"+lf.login.data)
            os.makedirs(os.getcwd()+"\\"+"users"+"\\"+lf.login.data+"\\"+"favourite_templates")
    return render_template('registration.html', form = lf, args=args)

@app.route('/make_admin/<string:username>')
def up_admin(username):
    um = UsersModel(db.get_connection())
    um.update(user_name=username, rights="admin")
    return "OK"

@app.route('/worker/<string:username>')
def up_worker(username):
    um = UsersModel(db.get_connection())
    um.update(user_name=username, rights="worker")
    return "OK"


@app.route('/forgot_login', methods=["GET", "POST"])
def forgot_login():
    fp = ForgotForm()
    us = UsersModel(db.get_connection())
    if (request.method=="POST"):

        if (us.find_email(fp.email.data)[0]):
            fromaddr = "pauchan.mobile@gmail.com"
            toaddr = fp.email.data
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Логин на сайте pauchan.pythonanywhere.com"
            body = "Ваш логин на сайте pauchan.pythonanywhere.com\n"+us.get_user(fp.email.data)[0]
            print(body)
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login('pauchan.mobile@gmail.com', 'pzqorfulfgihbxuf')
            server.sendmail(fromaddr, toaddr, text)
        return render_template("forgot_login.html", text="email_was_sent")
    else:
        return render_template("forgot_login.html", text="write_email", form = fp)

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    fp = ForgotForm()
    us = UsersModel(db.get_connection())
    if (request.method=="POST"):
        b = False
        if (fp.email.data.find('@')!=-1):
            email = fp.email.data
            username = us.get_user(email)
            b = True
        else:
            username = fp.email.data
            email = us.get_email(username)
        if (username!=None and email!=None):
                if (b):
                    username=username[0]
                else:
                    email = email[0]
                fromaddr = "pauchan.mobile@gmail.com"
                toaddr = email
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Смена пароля на сайте pauchan.pythonanywhere.com"
                body = "Если вы хотите сменить пароль перейдите по ссылке ниже:\n" + "http://127.0.0.1:5000/reset_password/" +  username
                print (body)
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login('pauchan.mobile@gmail.com', 'pzqorfulfgihbxuf')
                server.sendmail(fromaddr, toaddr, text)
        return render_template("forgot_password.html", text="email_was_sent")
    else:
        return render_template("forgot_password.html", text="write_email", form = fp)

@app.route('/reset_password/<string:username>', methods=["GET", "POST"])
def reset_password(username):
    print(username)
    rf = ResetPassword()
    args = []
    if request.method=="POST":
        um = UsersModel(db.get_connection())
        if (um.exists(username, rf.new_password.data))[0]:
            args+=["Exists"]
        else:
            args+=["OK"]
            um.update(user_name=username, password=rf.new_password.data)
    return render_template("reset_password.html", args = args, form = rf)

@app.route("/profile")
def profile():
    return "KEK"

@app.route('/login', methods=["GET", "POST"])
def login():
    lf = LoginForm()
    us = UsersModel(db.get_connection())
    args = []
    if (request.method == "POST"):
        if (us.exists(lf.username.data, lf.password.data))[0]:
            session['username']=lf.username.data
            session['rights'] = us.get_pole(username = lf.username.data, rights = "")
            return profile()
        else:
            return render_template("login.html", args=["not exists"], form = lf)
    return render_template("login.html", form = lf)



if __name__ == '__main__':
    app.run(debug=True)
