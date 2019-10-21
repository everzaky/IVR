from flask import Flask, render_template, request, session, redirect, url_for
from users_model import UsersModel
from db import DB
from category_model import CategoryModel
from product_model import ProductModel
from shop_model import ShopModel
from shop_db import DB_SHOP
from shop_product_model import ProductShopModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from country_model import CountryModel
from producer_model import ProducerModel
from forms import *
import smtplib
import os
import datetime
import shutil
import json
import itertools


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
            return redirect('/search/search/'+sm.value.data)
    else:
        cm = CategoryModel(db.get_connection())
        categories = cm.get_all()
        return render_template("index.html", session=session, categories=categories, form2 = sm)


@app.route('/create_category', methods=["GET", "POST"])
def create_category():
    CF = CategoryForm()
    CM = CategoryModel(db.get_connection())
    if (request.method=="POST"):
        name_category = CF.NameCategory.data
        if (CM.exists(name_category)):
            return render_template('category.html', args=["Exists"], form = CF)
        else:
            CM.insert(name_category," ")
            return render_template('category.html', args=["Done"], form = CF)

    else:
        return render_template('category.html', args=["kek"], form = CF)

@app.route('/show/category')
def show_categories():
    cm = CategoryModel(db.get_connection())
    categories = cm.get_all()
    items = [ [i[1], i[0]] for i in categories]
    items.sort()
    return render_template("work_with_categories.html", items = items)

@app.route('/update/category/<int:id>', methods=["GET", "POST"])
def update_category(id):
    cm = CategoryModel(db.get_connection())
    cf = RecreateCategoryForm()
    args = []
    if (request.method=="POST"):
        name_category = cf.NameCategory.data
        if (len(cf.NameCategory.data)!=0):
            if (cm.exists(name_category)):
                args+=["Exists"]
                return render_template('recreate_category.html', form = cf, args=args)
            else:
                cm.update(id = id, name_of_category=name_category)
                return redirect('/show/category')
    return render_template('recreate_category.html', args=args, form =cf)

def del_product(id):
    pm = ProductModel(db.get_connection())
    shops = os.listdir(os.getcwd() + "\\static\\shops")
    product = pm.get(id)
    images = product[7].split()
    for image in images:
        os.remove(os.getcwd() + "\\static\\img\\" + image)
    pm.delete(id)
    for shop in shops:
        shop_db = DB_SHOP(shop)
        shop_product = ProductShopModel(shop_db.get_connection()).init_table()
        if shop_product.exists(id):
            shop_product.delete(id)

@app.route('/delete/category/<int:id>')
def delete_category(id):
    Cm = CategoryModel(db.get_connection())
    products = Cm.get_products(id)[0].split()
    for product in products:
        del_product(int(product))
    Cm.delete(id)
    return redirect("/show/category")

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

@app.route('/update/country/<int:id>', methods=["GET", "POST"])
def update_country(id):
    rcf = RecreateCountryForm()
    ctm = CountryModel(db.get_connection())
    args=[]
    if (request.method=="POST"):
        if (len(rcf.name.data)!=None):
            ctm.update(id, name_of_country=rcf.name.data)
        print(rcf.flag.data)
        return "kek"
    else:
        return render_template('recreate_country.html', form = rcf, args = args)

@app.route('/delete/country/<int:id>', methods=["GET", "POST"])
def delete_country(id):
    ctm = CountryModel(db.get_connection())
    products = ctm.get_products(id)[0].split()
    for product in products:
        del_product(product)
    ctm.delete(id)
    return redirect('/show/country')

@app.route('/show/country')
def show_countries():
    ctm = CountryModel(db.get_connection())
    countries = ctm.get_all()
    countries = [[i[1], i[0]] for i in countries]
    countries.sort()
    return render_template('work_with_countries.html', countries=countries)


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
            images = ""
            i = 1
            id_category = CM.get_id(Pf.select.data)[0]
            id_producer = prm.get_id(Pf.producer.data)[0]
            id_country = conm.get_id(Pf.country.data)[0]
            for img in Pf.file.data:
                trash = img.filename.split(".")
                img.filename = "_".join(Pf.name.data.split())+"_"+str(i)+"."+trash[len(trash)-1]
                print(img.filename)
                i+=1
                images+=img.filename+" "
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], img.filename))
            pm.insert(Pf.name.data, Pf.price.data, 0, False, str(datetime.datetime.now()), str(datetime.datetime.now()),
                      images, Pf.text.data, id_country, id_producer, id_category)
            id_product = pm.get_id(Pf.name.data)[0]
            products = CM.get_products(id_category)[0]
            products+=" "+str(id_product)
            print(products)
            CM.update(id=id_category, products=products)
            products = conm.get_products(id_country)[0]
            products+=" "+str(id_product)
            print(products)
            conm.update(id = id_country,  products=products)
            products = prm.get_products(id_producer)[0]
            products+=" "+str(id_product)
            prm.update(id = id_producer, products=products)
            args+=["OK"]
    return render_template("product.html", form = Pf, args = args)

@app.route('/delete/product/<int:id>/<string:ret_url>')
def delete_product(id, ret_url):
    pm= ProductModel(db.get_connection())
    shops = os.listdir(os.getcwd()+"\\static\\shops")
    product = pm.get(id)
    images = product[7].split()
    for image in images:
        os.remove(os.getcwd()+"\\static\\img\\"+image)
    pm.delete(id)
    for shop in shops:
        shop_db = DB_SHOP(shop)
        shop_product = ProductShopModel(shop_db.get_connection()).init_table()
        if shop_product.exists(id):
            shop_product.delete(id)
    ret_url='/'.join(ret_url.split(" "))
    return redirect(ret_url)

@app.route('/search/<string:filter>/<string:value>')
def search(filter, value):
    res = dict()
    if (filter=="category"):
        cm = CategoryModel(db.get_connection())
        name_of_category = cm.get(int(value))[1]
        pm = ProductModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        prm = ProducerModel(db.get_connection())
        products = cm.get_products(int(value))[0].split()
        items = []
        product=" "
        for i in products:
            item = pm.get(int(i))
            if (item!=None):
                product+=i+" "
                print(item)
                item = [item[0], item[1], item[2], item[3], item[4], item[7].split()[0], item[8], ctm.get(item[9])[1], prm.get(item[10])[1], ctm.get_flag(item[9])[0]]
                items+=[item]
        cm.update(id = int(value), products=product)
        res["category_result"]=[items,name_of_category, (len(items)>0)]
    if (filter=="country"):
        pm = ProductModel(db.get_connection())
        cm = CategoryModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        prm = ProducerModel(db.get_connection())
        items = []
        name_of_country = ctm.get(int(value))[1]
        products = ctm.get_products(int(value))[0].split()
        product=" "
        for i in products:
            item = pm.get((int(i)))
            if (item!=None):
                product+=i+" "
                item = [item[0], item[1], item[2], item[3], item[4], item[7].split()[0], item[8], cm.get(item[11])[1], prm.get(item[10])[1]]
                items+=[item]
        ctm.update(id=int(value), products=product)
        res["country_result"] = [items, name_of_country, (len(items) > 0), ctm.get_flag(int(value))[0]]
    if (filter=="producer"):
        pm = ProductModel(db.get_connection())
        cm = CategoryModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        prm = ProducerModel(db.get_connection())
        items = []
        name_of_producer = prm.get(int(value))[1]
        products=prm.get_products(int(value))[0].split()
        product = " "
        for i in products:
            item = pm.get(int(i))
            if (item!=None):
                product+=i+" "
                item = [item[0], item[1], item[2], item[3], item[4], item[7].split()[0], item[8], ctm.get(item[9])[1], cm.get(item[11])[1], ctm.get_flag(item[9])[0]]
                items+=[item]
        prm.update(int(value), products=product)
        res["producer_result"]=[items, name_of_producer, (len(items)>0)]
    if (filter=="search"):
        pm = ProductModel(db.get_connection())
        cm = CategoryModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        prm = ProducerModel(db.get_connection())
        categories = cm.get_all()
        category_items=[]
        for category in categories:
            if (category[1].find(value)!=-1):
                category_items+=[category[0], category[1]]
        category_result = [[category_items], (len(category_items)>0)]
        producers = prm.get_all()
        producer_items = []
        for producer in producers:
            if (producer[1].find(value)!=-1):
                producer_items+=[producer[0], producer[1]]
        producer_result = [[producer_items], (len(producer_items)>0)]
        countries = ctm.get_all()
        countries_items = []
        for country in countries:
            if (country[1].find(value)!=-1):
                countries_items+=[country[0], country[1]]
        country_result=[[countries_items], (len(countries_items)>0)]
        products=pm.get_all()
        product_items = []
        for product in products:
            if (product[1].find(value)!=-1):
                product_items+=[product[0], product[1], product[2], product[3], product[4], product[7].split()[0], product[8], ctm.get(product[9])[1], ctm.get_flag(product[9])[0], prm.get(product[10])[1], cm.get(product[11])[1]]
        product_result = [[product_items], (len(product_items)>0)]
        search_result = [category_result, producer_result, country_result, product_result]
        res["search_result"]=[search_result, search_result[0][1] or search_result[1][1] or search_result[2][1] or search_result[3][1]]
    url = " search "+str(filter)+" "+str(value)
    return render_template('search_result.html', res = res, url=url)

@app.route('/delete/shop/<int:id>')
def delete_shop(id):
    sm = ShopModel(db.get_connection())
    name = sm.get(id)[1]
    shutil.rmtree(os.getcwd()+"\\static\\shops\\"+name)
    sm.delete(id)
    return redirect('/show/shop')

@app.route('/choose/shop/<int:id>', methods=["GET", "POST"])
def choose_product_shop(id):
    cf = ChooseProduct()
    args = []
    if (request.method=="POST"):
        pm = ProductModel(db.get_connection())
        if (pm.exists(cf.select2.data)[0]):
            id_pr=pm.get_id(cf.select2.data)[0]
            return redirect('/pos/product/'+str(id_pr)+"/shop/"+str(id))
        else:
            cm = CategoryModel(db.get_connection())
            products = cm.get_products(cm.get_id(cf.select1.data)[0])[0].split()
            productss = ""
            choices = []
            for product in products:
                if (pm.get(int(product))!=()):
                    choices += [pm.get(int(product))[1]]
                    productss += product+" "
            cm.update(id = cm.get_id(cf.select1.data)[0], products=productss)
            cf.select2.choices = choices
            args+=["choose_product"]
            return render_template('choose_product.html', form=cf, url='/show/shop', args=args)
    else:
        args=["choose_category"]
        cm = CategoryModel(db.get_connection())
        categories = cm.get_all()
        categories = [i[1] for i in categories]
        cf.select1.choices=categories
        return render_template('choose_product.html', form=cf, url = '/show/shop', args=args)


@app.route('/pos/product/<int:id_pr>/shop/<int:id_sh>', methods=["GET", "POST"])
def pos_product(id_pr, id_sh):
    psf = PosProduct()
    pm = ProductModel(db.get_connection())
    name_of_product = pm.get(id_pr)[1]
    sm = ShopModel(db.get_connection())
    name_of_shop = sm.get(id_sh)[1]
    db_shop = DB_SHOP(name_of_shop)
    ProductShopModel(db.get_connection()).init_table()
    shop_product_model = ProductShopModel(db_shop.get_connection())
    id_product = shop_product_model.get_id(name_of_product)
    if (type(id_product).__name__=='NoneType'):
        shop_product_model.insert(name_of_product, location='', number_of_product=0)
        shop_product_model = ProductShopModel(db_shop.get_connection())
    if (request.method == "POST"):
        id_product = shop_product_model.get_id(name_of_product)[0]
        if (type(psf.number.data).__name__!='NoneType'):
            shop_product_model.update(id=int(id_product), number_of_product=int(psf.number.data))
        shop_product_model.update(id = id_product, location=psf.output.data)
    id_product = shop_product_model.get_id(name_of_product)[0]
    product=shop_product_model.get(id_product)
    product_number = product[3]
    locations = product[2]
    if (type(locations).__name__!='NoneType' and locations!=''):
        s=locations
        s=s[0:len(s)-1]
        pos_products = [[int(i.split(':')[0]), [list(map(str, j.split("|"))) for j in i.split(':')[1].split()]] for i in
                    s.split('_')]
    else:
        pos_products=[]
    images = os.listdir(os.getcwd()+'\\static\\shops\\'+name_of_shop+"\\img")
    images = [[i,[]] for i in images]
    for i in pos_products:
        for j in i[1]:
            images[i[0]][1].append(j)
    print(images)
    url = '/pos/product/'+str(id_pr)+'/shop/'+str(id_sh)+"?"
    return render_template('pos_product.html', form = psf, name = name_of_product, number = product_number, images=images, name_of_shop=name_of_shop, url = url)

@app.route('/show/shop')
def show_shop():
    sm = ShopModel(db.get_connection())
    shops = sm.get_all()
    shops = [[i[1], i[0] , i[2]] for i in shops]
    shops.sort()
    return render_template('work_with_shops.html', shops = shops)

@app.route('/create/shop', methods = ["GET", "POST"])
def create_shop():
    csf = CreateShopForm()
    sm = ShopModel(db.get_connection())
    args = []
    if (request.method=="POST"):
        if (sm.exists(csf.name.data)[0]):
            args+=["name_exists"]
        else:
            os.makedirs(os.getcwd()+"\\static\\shops\\"+csf.name.data)
            os.makedirs(os.getcwd()+"\\static\\shops\\"+csf.name.data+"\\"+"img")
            i=1
            sm.insert(csf.name.data, csf.location.data)
            id = sm.get_id(csf.name.data)[0]
            for img in csf.files.data:
                trash = img.filename.split(".")
                img.filename = str(id)+"_"+str(i)+'.'+trash[len(trash)-1]
                i += 1
                img.save(os.path.join(os.getcwd()+"\\static\\shops\\"+csf.name.data+"\\"+"img", img.filename))
            db_shop = DB_SHOP(csf.name.data)
            shop_product = ProductShopModel(db_shop.get_connection()).init_table()
            args+=["OK"]
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
            return redirect('/profile')
        else:
            args+=["not_exists"]
    return render_template("login.html", form = lf, args=args)

@app.route('/exit')
def ex():
    del session['username']
    del session['rights']
    return redirect('/')

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

@app.errorhandler(403)
def wrong(e):
    return "Извините разработчик плохо продумал систему", 403

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True)
