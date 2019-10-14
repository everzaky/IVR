from flask import Flask, render_template, request, session, redirect
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
from shop_product_model import ProductShopModel
from add_favourite_product_form import AddFavProduct
from reset_password_form import ResetPassword
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from country_model import CountryModel
from country_form import CountryForm
from producer_form import ProducerForm
from producer_model import ProducerModel
from search_form import SearchForm
import smtplib
import os
import datetime
import shutil


app = Flask(__name__ , static_folder="D:\E1\IVR\server\static")
db = DB()

UsersModel(db.get_connection()).init_table()
CategoryModel(db.get_connection()).init_table()
ProductModel(db.get_connection()).init_table()
ShopModel(db.get_connection()).init_table()
CountryModel(db.get_connection()).init_table()
ProducerModel(db.get_connection()).init_table()

app.config['SECRET_KEY'] = 'nothing'
app.config['UPLOAD_FOLDER']="D:\\E1\\IVR\\server\\static\\img"

#smtpObj.login('pauchan.mobile@mail.ru', 'YS8-pY8-ZZr-JSG')
print("fff")

@app.route("/", methods=["GET", "POST"])
def index():
    sm = SearchForm()
    if (request.method=="POST"):
            return redirect('/search/search/'+sm.value)
    else:

        cm = CategoryModel(db.get_connection())
        musor = cm.get_all()
        categories = [i[1] for i in musor]
        return render_template("index.html", session=session, categories=categories)

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

@app.route('/work_with_categories')
def work_with_category():
    cm = CategoryModel(db.get_connection())
    categories = cm.get_all()
    items = [ (i[0], i[1]) for i in categories]
    return render_template("work_with_categories.html", items = items)

@app.route('/create/product', methods=["GET", "POST"])
def create_product():
    CM = CategoryModel(db.get_connection())
    categories = CM.get_all()
    categories = [i[1] for i in categories]
    Pf = ProductForm()
    Pf.select.choices=categories
    pm = ProductModel(db.get_connection())
    conm = CountryModel(db.get_connection())
    countries = conm.get_all()
    countries =[i[1] for i in countries]
    Pf.country.choices = countries
    prm = ProducerModel(db.get_connection())
    producers = prm.get_all()
    producers=[i[1] for i in producers]
    Pf.producer.choices = producers
    args = []
    if request.method=="POST":
        if (pm.exists(Pf.name.data)[0]):
            args+=["Exists"]

        else:
            products = CM.get_products(Pf.select.data)[0]
            products+=" "+Pf.name.data
            print(products)
            CM.update(name_of_category=Pf.select.data, products=products)
            products = conm.get_products(Pf.country.data)[0]
            products+=" "+Pf.name.data
            conm.update(name_of_country=Pf.country.data, products=products)
            products = prm.get_products(Pf.producer.data)[0]
            products+=" "+Pf.name.data
            prm.update(name_of_producer=Pf.producer.data, products=products)
            images=""
            i = 1
            for img in Pf.file.data:
                trash = img.filename.split(".")
                img.filename = Pf.name.data+"_"+str(i)+"."+trash[len(trash)-1]
                print(img.filename)
                i+=1
                images+=img.filename+" "
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], img.filename))
            pm.insert(Pf.name.data, Pf.price.data, 0, False, str(datetime.datetime.now()), str(datetime.datetime.now()),
                      images, Pf.text.data, Pf.country.data, Pf.producer.data)
            args+=["OK"]
    return render_template("product.html", form = Pf, args = args)

@app.route('/search/<string:filter>/<string:value>')
def search(filter, value):
    res = dict()

    if (filter=="category"):
        cm = CategoryModel(db.get_connection())
        pm = ProductModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        products = cm.get_products(value)[0].split()
        items = [pm.get(product) for product in products]
        items = [[item, item[7].split()[0], ctm.get_flag(item[9])[0]] for item in items]
        print(items)
        res["category_result"] = [items, value]
        print(res["category_result"])
    return render_template('search_result.html', res = res)

def delete_product(name, ret_url):
    pm= ProductModel(db.get_connection())
    shops = os.listdir(os.getcwd()+"\\shops")
    pm.delete(name)
    for shop in shops:
        shop_db = DB_SHOP(shop)
        shop_product = ProductShopModel(shop_db.get_connection()).init_table()
        if shop_product.exists(name):
            shop_product.delete(name)
    return redirect(ret_url)

def del_product(name):
    pm = ProductModel(db.get_connection())
    shops = os.listdir(os.getcwd() + "\\static\\shops")
    pm.delete(name)
    for shop in shops:
        shop_db = DB_SHOP(shop)
        shop_product = ProductShopModel(shop_db.get_connection()).init_table()
        if shop_product.exists(name):
            shop_product.delete(name)

@app.route('/update/category/<int:id>', methods=["GET", "POST"])
def rename_category(id):
    cm = CategoryModel(db.get_connection())
    cf = CategoryForm()
    args = []
    if (request.method=="POST"):
        name_category = cf.NameCategory.data
        if (cm.exists(name_category)):
            args+=["Exists"]
            return render_template('rename_category.html', form = cf, args=args)
        else:
            cm.update(id = id, name_of_category=name_category)
            return redirect('/work_with_categories')
    else:
        return render_template('rename_category.html', args=args, form =cf)

@app.route('/delete/category/<string:name_category>')
def delete_category(name_category):
    Cm = CategoryModel(db.get_connection())
    products = Cm.get_products(name_category)[0].split()
    for product in products:
        del_product(product)
    Cm.delete(name_category)
    return redirect('/work_with_categories')

@app.route('/create/country', methods=["GET", "POST"])
def create_country():
    args=[]
    cm = CountryModel(db.get_connection())
    cf = CountryForm()
    if (request.method=="POST"):
        if (cm.exists(cf.name.data)[0]):
            args+=["exists"]
        else:
            img = cf.flag.data
            trash = img.filename.split('.')
            img.filename=cf.name.data+'.'+trash[len(trash)-1]
            cm.insert(cf.name.data, img.filename, ' ')
            img.save(os.getcwd()+"\\static\\countries\\"+img.filename)
            args+=["OK"]
    return render_template('create_country.html', args = args, form = cf)

@app.route('/create/producer/', methods=["GET", "POST"])
def create_producer():
    args = []
    pm = ProducerModel(db.get_connection())
    pf = ProducerForm()
    if (request.method == "POST"):
        if (pm.exists(pf.name.data)[0]):
            args += ["exists"]
        else:
            pm.insert(pf.name.data," ")
            args += ["OK"]
    return render_template('create_producer.html', args=args, form=pf)

def delete_shop(name):
    sm = ShopModel(db.get_connection())
    sm.delete(name)
    shutil.rmtree(os.getcwd()+"\\static\\shops\\"+name)



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
            i=1
            for img in csf.files.data:
                trash = img.filename.split(".")
                img.filename = csf.name.data + "_" + str(i) + "." + trash[1]
                i += 1
                img.save(os.path.join(os.getcwd()+"\\shops\\"+csf.name.data+"\\"+"img", img.filename))
            db_shop = DB_SHOP(csf.name.data)
            shop_product = ProductShopModel(db_shop.get_connection()).init_table()
            sm.insert(csf.name.data, csf.location.data)
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
            um.insert(lf.login.data, lf.email.data, lf.password.data, "user", ' ', lf.sales_notif.data, lf.sales_notif_fav_products.data)

            os.makedirs(os.getcwd()+"\\"+"users"+"\\"+lf.login.data)
            os.makedirs(os.getcwd()+"\\"+"users"+"\\"+lf.login.data+"\\"+"favourite_templates")
    return render_template('registration.html', form = lf, args=args)

@app.route('/make_admin/<string:username>')
def up_admin(username):
    um = UsersModel(db.get_connection())
    um.update(user_name=username, rights="admin")
    return "OK"

@app.route('/worker/<string:shop_name>/<string:username>')
def up_worker(shop_name,username):
    um = UsersModel(db.get_connection())
    um.update(user_name=username, rights="worker_"+shop_name)
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

@app.route('/favourite_products')
def favourite_products():
    username = session["username"]
    um = UsersModel(db.get_connection())
    products = um.get_products(username)[0].split()
    return render_template("favourite_products.html", products=products)

@app.route('/delete/favourite_products/<string:name>')
def delete_favourite_product(name):
    username = session["username"]
    um = UsersModel(db.get_connection())
    products = um.get_products(username)[0].split()
    products.pop(products.index(name))
    um.update(user_name=session["username"], favourite_products=' '.join(products))
    return redirect('/favourite_products')

@app.route('/add/favourite_products', methods=["GET", "POST"])
def add_favourite_product():
    afp = AddFavProduct()
    args = []
    um = UsersModel(db.get_connection())
    cm = CategoryModel(db.get_connection())
    if (request.method=="POST"):
        if (cm.exists(afp.select1.data)):
            products = cm.get_products(afp.select1.data)[0].split()
            args+=["choose_product"]
            afp.select2.choices=products
            return render_template("add_favourite_product.html", form=afp, args=args)

        else:
            favourite_products = um.get_products(session["username"])[0].split()
            if (afp.select2.data in favourite_products):
                args+=["exists"]
            else:
                args+=["OK"]
                favourite_products=' '.join(favourite_products+[afp.select2.data])
                um.update(user_name=session["username"], favourite_products=favourite_products)
            args += ["choose_category"]
            musor = cm.get_all()
            categories = [i[1] for i in musor]
            print(categories)
            afp.select1.choices = categories
            return render_template("add_favourite_product.html", form=afp, args=args)

    else:
        args+=["choose_category"]
        musor = cm.get_all()
        categories = [i[1] for i in musor]
        print(categories)
        afp.select1.choices=categories
        return render_template("add_favourite_product.html", form = afp, args = args)


@app.route("/profile")
def profile():
    return render_template("profile.html", session=session)

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
            return redirect("/profile")
    return render_template("login.html", form = lf)


@app.errorhandler(404)
def error(e):
    return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)
