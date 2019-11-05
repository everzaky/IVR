from flask import Flask, render_template, request, session, redirect, url_for, jsonify, Response, send_file
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
from PIL import Image
from decimal import Decimal
import smtplib
import os
import datetime
import shutil
import json
import itertools
import platform

slashes = ""

if platform.system() == "Windows":
    slashes = "\\"
else:
    slashes = "/"

print(os.getcwd())
app = Flask(__name__, static_folder=os.getcwd()+slashes+"static")
db = DB(slashes)

UsersModel(db.get_connection()).init_table()

CategoryModel(db.get_connection()).init_table()
ProductModel(db.get_connection()).init_table()
ShopModel(db.get_connection()).init_table()
CountryModel(db.get_connection()).init_table()
ProducerModel(db.get_connection()).init_table()

app.config['SECRET_KEY'] = 'nothing'
app.config['UPLOAD_FOLDER'] = os.getcwd()+slashes+"static"+slashes+"img"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# smtpObj.login('pauchan.mobile@mail.ru', 'YS8-pY8-ZZr-JSG')

@app.route("/",
           methods=["GET", "POST"])
def index():
    sm = SearchForm()
    if request.method == "POST":
        return redirect('/search/search/'+sm.value.data)
    else:
        cm = CategoryModel(db.get_connection())
        categories = cm.get_all()
        return render_template("index.html", session=session, categories=categories, form2=sm)

@app.route('/create_category',
           methods=["GET", "POST"])
def create_category():
    cf = CategoryForm()
    cm = CategoryModel(db.get_connection())
    if request.method == "POST":
        name_category = cf.NameCategory.data
        if cm.exists(name_category):
            return render_template('category.html', args=["Exists"], form=cf)
        else:
            cm.insert(name_category, " ")
            return render_template('category.html', args=["Done"], form=cf)
    else:
        return render_template('category.html', args=["kek"], form=cf)

@app.route('/show/category'
           )
def show_categories():
    cm = CategoryModel(db.get_connection())
    categories = cm.get_all()
    items = [[i[1], i[0]] for i in categories]
    items.sort()
    return render_template("work_with_categories.html", items=items)

@app.route('/update/category/<int:id>',
           methods=["GET", "POST"])
def update_category(id):
    cm = CategoryModel(db.get_connection())
    cf = RecreateCategoryForm()
    args = []
    if request.method == "POST":
        name_category = cf.NameCategory.data
        if len(cf.NameCategory.data) != 0:
            if cm.exists(name_category):
                args += ["Exists"]
                return render_template('recreate_category.html', form=cf, args=args)
            else:
                cm.update(id=id, name_of_category=name_category)
                return redirect('/show/category')
    return render_template('recreate_category.html', args=args, form=cf)

def del_product(id):
    pm = ProductModel(db.get_connection())
    shops = os.listdir(os.getcwd() + slashes + "static"+slashes + "shops")
    product = pm.get(id)
    images = product[6].split()
    for image in images:
        print(image)
        os.remove(os.getcwd() + slashes + "static" + slashes + "img" + slashes+ image)
    pm.delete(id)
    for shop in shops:
        shop_db = DB_SHOP(shop, slashes)
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
            img.save(os.getcwd()+slashes+"static" + slashes +"countries"+slashes+img.filename)
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

            print(type(Pf.price.data), type(Decimal("0.0")))
            print(type(Pf.name.data), type(Pf.price.data), type(Decimal('0.0')), type(str(datetime.datetime.now)), type(datetime.datetime.now()), type(images), type(Pf.text.data), type(id_country), type(id_producer), type(id_category))
            pm.insert(Pf.name.data, Pf.price.data, float(0), str(datetime.date(year=2018, month=1, day=1)), str(datetime.datetime.now()),
                      "", Pf.text.data, id_country, id_producer, id_category)
            id_product = pm.get_id(Pf.name.data)[0]
            images = ""
            i=1
            for img in Pf.file.data:
                trash = img.filename.split(".")
                img.filename = str(id_product)+"_"+str(i)+"."+trash[len(trash)-1]
                i+=1
                images+=img.filename+" "
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], img.filename))
            pm.update(id = id_product, list_of_photos = images)
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
    shops = os.listdir(os.getcwd()+slashes+"static"+slashes+"shops")
    product = pm.get(id)
    name_of_product = product[1]
    images = product[6].split()
    for image in images:
        print(image)
        os.remove(os.getcwd()+slashes+"static"+slashes+"img"+slashes+image)

    for shop in shops:
        shop_db = DB_SHOP(shop, slashes)
        ProductShopModel(shop_db.get_connection()).init_table()
        shop_product=ProductShopModel(shop_db.get_connection())
        if type(shop_product.get_id(name_of_product)).__name__!="NoneType":
            shop_product.delete(shop_product.get_id(name_of_product)[0])
    pm.delete(id)
    ret_url='/'.join(ret_url.split(" "))
    return redirect(ret_url)

@app.route('/search/<string:filter>/<string:value>')
def search(filter, value):
    res = dict()
    sm = ShopModel(db.get_connection())
    shops = sm.get_all()
    shops = [[i[1], i[0]] for i in  shops]
    shops.sort()
    list_of_shablons=[]
    shablons_true=False
    if "username" in session.keys():
        shablons_true=True
        list_of_shablons = os.listdir(os.getcwd()+slashes+"users"+slashes+session['username'] +slashes+"favourite_templates")
        list_of_shablons=[i[0:len(i)-4] for i in list_of_shablons]

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
                item = [item[0], item[1], item[2], item[3], item[4], item[5],  item[6].split()[0], item[7], ctm.get(item[8])[1], prm.get(item[9])[1], ctm.get_flag(item[8])[0]]
                av_shop = []
                for shop in shops:
                    db_shop=DB_SHOP(shop[0], slashes)
                    ProductShopModel(db_shop.get_connection()).init_table()
                    shop_model=ProductShopModel(db_shop.get_connection())
                    id_pr=shop_model.get_id(item[1])
                    if (type(id_pr).__name__!="NoneType"):
                        av_shop+=[shop]
                item+=[av_shop]
                items+=[item]
                print(item)
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
                item = [item[0], item[1], item[2], item[3], item[4], item[5], item[6].split()[0], item[7], cm.get(item[10])[1], prm.get(item[9])[1]]
                av_shop = []
                for shop in shops:
                    db_shop = DB_SHOP(shop[0], slashes)
                    ProductShopModel(db_shop.get_connection()).init_table()
                    shop_model = ProductShopModel(db_shop.get_connection())
                    id_pr = shop_model.get_id(item[1])
                    if (type(id_pr).__name__ != "NoneType"):
                        av_shop += [shop]
                item += [av_shop]
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
                item = [item[0], item[1], item[2], item[3], item[4], item[5], item[6].split()[0], item[7], ctm.get(item[8])[1], cm.get(item[10])[1], ctm.get_flag(item[8])[0]]
                av_shop = []
                for shop in shops:
                    db_shop = DB_SHOP(shop[0], slashes)
                    ProductShopModel(db_shop.get_connection()).init_table()
                    shop_model = ProductShopModel(db_shop.get_connection())
                    id_pr = shop_model.get_id(item[1])
                    if (type(id_pr).__name__ != "NoneType"):
                        av_shop += [shop]
                item += [av_shop]
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
                av_shop = []
                for shop in shops:
                    db_shop = DB_SHOP(shop[0], slashes)
                    ProductShopModel(db_shop.get_connection()).init_table()
                    shop_model = ProductShopModel(db_shop.get_connection())
                    id_pr = shop_model.get_id(product[1])
                    if (type(id_pr).__name__ != "NoneType"):
                        av_shop += [shop]
                print([product[0], product[1], product[2], product[3], product[4], product[5],
                       product[6].split()[0], product[7], ctm.get(product[8])[1],
                       ctm.get_flag(product[8])[0], prm.get(product[9])[1], cm.get(product[10])[1], av_shop])
                product_items += [[product[0], product[1], product[2], product[3], product[4], product[5],
                                  product[6].split()[0], product[7], ctm.get(product[8])[1],
                                  ctm.get_flag(product[8])[0], prm.get(product[9])[1], cm.get(product[10])[1], av_shop]]
        product_result = [[product_items], (len(product_items)>0)]
        search_result = [category_result, producer_result, country_result, product_result]
        res["search_result"]=[search_result, search_result[0][1] or search_result[1][1] or search_result[2][1] or search_result[3][1]]
        print(res)
    url = " search "+str(filter)+" "+str(value)
    print(datetime.date.today())
    return render_template('search_result.html', res = res, url=url, shops = shops, date=str(datetime.date.today()), list_of_shablons=list_of_shablons, shablons_true=shablons_true)

@app.route('/delete/shop/<int:id>')
def delete_shop(id):
    sm = ShopModel(db.get_connection())
    name = sm.get(id)[1]
    shutil.rmtree(os.getcwd()+slashes+"static"+slashes+"shops"+slashes+name)
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
            return redirect('/pos/product/'+str(id_pr)+"/shop/"+str(id)+"/ show shop")
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

@app.route('/pos/product/<int:id_pr>/shop/<int:id_sh>/<string:ret_url>', methods=["GET", "POST"])
def pos_product(id_pr, id_sh, ret_url):
    psf = PosProduct()
    pm = ProductModel(db.get_connection())
    name_of_product = pm.get(id_pr)[1]
    sm = ShopModel(db.get_connection())
    name_of_shop = sm.get(id_sh)[1]
    db_shop = DB_SHOP(name_of_shop, slashes)
    ProductShopModel(db.get_connection()).init_table()
    shop_product_model = ProductShopModel(db_shop.get_connection())
    id_product = shop_product_model.get_id(name_of_product)
    if (type(id_product).__name__=='NoneType'):
        price = pm.get(id_pr)[2]
        shop_product_model.insert(name_of_product, location='', number_of_product=0, price=price, price_sale=0, date_of_end=(datetime.date.today()), date_of_start=(datetime.date.today()))
        shop_product_model = ProductShopModel(db_shop.get_connection())
    if (request.method == "POST"):
        id_product = shop_product_model.get_id(name_of_product)[0]
        if (type(psf.number.data).__name__!='NoneType'):
            shop_product_model.update(id=int(id_product), number_of_product=int(psf.number.data))
        if (type(psf.price.data).__name__!='NoneType'):
            shop_product_model.update(id=int(id_product), price=(psf.price.data))
        shop_product_model.update(id = id_product, location=psf.output.data)
    id_product = shop_product_model.get_id(name_of_product)[0]
    product=shop_product_model.get(id_product)
    product_number = product[3]
    locations = product[2]
    price = product[4]
    if (type(locations).__name__!='NoneType' and locations!=''):
        s=locations
        s=s[0:len(s)-1]
        pos_products = [[int(i.split(':')[0]), [list(map(str, j.split("|"))) for j in i.split(':')[1].split()]] for i in
                        s.split('_')]
    else:
        pos_products=[]
    images = os.listdir(os.getcwd()+slashes+'static'+slashes+'shops'+slashes+name_of_shop+slashes+"img")
    imagess = []
    for i in images:
        im = Image.open(os.getcwd()+slashes+'static'+slashes+'shops'+slashes+name_of_shop+slashes+"img"+slashes+i)
        width, height = im.size
        print(width, height)
        imagess.append([i, width, height, []])
    images=imagess
    for i in pos_products:
        for j in i[1]:
            images[i[0]][3].append(j)
    print(images)
    url = '/pos/product/'+str(id_pr)+'/shop/'+str(id_sh)+"?"
    ret_url="/".join(ret_url.split(" "))
    return render_template('pos_product.html', form = psf, name = name_of_product, number = product_number, images=images, name_of_shop=name_of_shop, url = url, ret_url=ret_url, price=price)

@app.route('/show/position/<int:id_pr>/shop/<int:id_sh>/<string:ret_url>', methods=["GET", "POST"])
def show_pos(id_pr, id_sh, ret_url):
    pm = ProductModel(db.get_connection())
    name_of_product = pm.get(id_pr)[1]
    sm = ShopModel(db.get_connection())
    name_of_shop = sm.get(id_sh)[1]
    db_shop = DB_SHOP(name_of_shop, slashes)
    ProductShopModel(db.get_connection()).init_table()
    shop_product_model = ProductShopModel(db_shop.get_connection())
    id_product = shop_product_model.get_id(name_of_product)[0]
    product = shop_product_model.get(id_product)
    product_number = product[3]
    locations = product[2]
    price = product[4]
    if (type(locations).__name__ != 'NoneType' and locations != ''):
        s = locations
        s = s[0:len(s) - 1]
        pos_products = [[int(i.split(':')[0]), [list(map(str, j.split("|"))) for j in i.split(':')[1].split()]] for i in
                        s.split('_')]
    else:
        pos_products = []
    images = os.listdir(os.getcwd() + slashes + 'static' + slashes + 'shops' + slashes + name_of_shop + slashes + "img")
    imagess = []
    for i in images:
        im = Image.open(
            os.getcwd() + slashes + 'static' + slashes + 'shops' + slashes + name_of_shop + slashes + "img" + slashes + i)
        width, height = im.size
        imagess.append([i, width, height, []])
    images = imagess
    for i in pos_products:
        for j in i[1]:
            images[i[0]][3].append(j)
    item=[product[1], product[4], product[5], product[6], product[7], product_number]
    print(item)
    ret_url = '/'.join(ret_url.split(" "))
    return render_template('show_pos_product.html', time=str(datetime.date.today()), item=item, ret_url=ret_url, images=images, name_of_shop=name_of_shop)

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
            os.makedirs(os.getcwd()+slashes+"static"+slashes+"shops"+slashes+csf.name.data)
            os.makedirs(os.getcwd()+slashes+"static"+slashes+"shops"+slashes+csf.name.data+slashes+"img")
            i=1
            sm.insert(csf.name.data, csf.location.data)
            id = sm.get_id(csf.name.data)[0]
            for img in csf.files.data:
                trash = img.filename.split(".")
                img.filename = str(id)+"_"+str(i)+'.'+trash[len(trash)-1]
                i += 1
                img.save(os.path.join(os.getcwd()+slashes+"static"+slashes+"shops"+slashes+csf.name.data+slashes+"img", img.filename))
            db_shop = DB_SHOP(csf.name.data, slashes)
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
            os.makedirs(os.getcwd()+slashes+"users"+slashes+lf.login.data)
            os.makedirs(os.getcwd()+slashes+"users"+slashes+lf.login.data+slashes+"favourite_templates")
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

@app.route('/show/fav/products')
def favourite_products():
    username = session["username"]
    um = UsersModel(db.get_connection())
    products = um.get_products(username)[0].split()
    pm = ProductModel(db.get_connection())
    product = " "
    productss=[]
    for i in products:
        item = pm.get(int(i))
        print(item)
        if len(item)>0:
            productss.append([item[1], item[0]])
            product+=i+" "
    print(productss)
    um.update(user_name=username, favourite_products=product)
    return render_template("favourite_products.html", products=productss)

@app.route('/delete/favourite_products/<int:id>')
def delete_favourite_product(id):
    username = session["username"]
    um = UsersModel(db.get_connection())
    products = um.get_products(username)[0].split()
    print(products)
    products.pop(products.index(str(id)))

    um.update(user_name=session["username"], favourite_products=' '.join(products)+" ")
    return redirect('/show/fav/products')

@app.route('/add/fav/products/<int:id>/<string:ret_url>', methods = ["GET"])
def add_fav_product_search(id, ret_url):
    username = session["username"]
    um = UsersModel(db.get_connection())
    products = um.get_pole(username = username, favourite_products=" ")[0].split()
    try:
        products.index(str(id))
    except ValueError:
        products=" ".join(products)+" "+str(id)
        um.update(user_name = username, favourite_products=products)
    ret_url='/'.join(ret_url.split(" "))
    return redirect(ret_url)

@app.route('/add/fav/products', methods = ["GET", "POST"])
def add_fav_product():
    cf = ChooseProduct()
    args = []
    args+=["favproducts"]
    if (request.method == "POST"):
        pm = ProductModel(db.get_connection())
        if (pm.exists(cf.select2.data)[0]):
            id_pr = pm.get_id(cf.select2.data)[0]
            um = UsersModel(db.get_connection())
            username = session["username"]
            favourite_products = um.get_products(username)[0].split()
            try:
                favourite_products.index(str(id_pr))
                args += ["exists"]
            except ValueError:
                favourite_products = " ".join(favourite_products) + " "+str(id_pr)
                args += ["OK"]
                um.update(user_name=username, favourite_products=favourite_products)
            args += ["choose_category"]
            cm = CategoryModel(db.get_connection())
            categories = cm.get_all()
            categories = [i[1] for i in categories]
            cf.select1.choices = categories
            cf.select2.data = None
            return render_template('choose_product.html', form=cf, url='/show/fav/products', args=args)
        else:
            cm = CategoryModel(db.get_connection())
            products = cm.get_products(cm.get_id(cf.select1.data)[0])[0].split()
            productss = ""
            choices = []
            for product in products:
                if (pm.get(int(product)) != ()):
                    choices += [pm.get(int(product))[1]]
                    productss += product + " "
            cm.update(id=cm.get_id(cf.select1.data)[0], products=productss)
            cf.select2.choices = choices
            args += ["choose_product"]
            return render_template('choose_product.html', form=cf, url='/show/fav/products', args=args)
    else:
        args = ["choose_category"]
        cm = CategoryModel(db.get_connection())
        categories = cm.get_all()
        categories = [i[1] for i in categories]
        cf.select1.choices = categories
        return render_template('choose_product.html', form=cf, url='/show/fav/products', args=args)

@app.route('/show/shablons', methods = ["GET", "POST"])
def show_shablons():
    username = session['username']
    shablons=os.listdir(os.getcwd()+slashes+"users"+slashes+username+slashes+"favourite_templates")
    shablons=[i[0:len(i)-4] for i in shablons]
    return render_template('work_with_shablons.html', shablons=shablons, url=" show shablons")

@app.route('/change/shablon/<string:name>/<string:ret_url>', methods=["GET", "POST"])
def change_shablon(name, ret_url):
    products = []
    file = open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt",'r')
    pm = ProductModel(db.get_connection())
    s=""
    for line in file:
        product = line.strip().split()
        item = pm.get(product[0])
        if (len(item)>0):
            s+=" ".join(product)+"\n"
            products+=[[item[0], item[1],product[1]]]
    print(products)
    file.close()
    file = open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt",'w')
    file.write(s)
    file.close()
    url1 = '/'.join(ret_url.split(" "))
    url = " change shablon "+name+"|"+ret_url
    print(url)
    return render_template('work_with_shablon.html', products=products, name=name, ret_url=url1, url=url, time=str(datetime.datetime.now()))

@app.route('/delete/shablon/<string:name>/<string:ret_url>', methods=["GET", "POST"])
def delete_shablon(name, ret_url):
    os.remove(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt")
    url = '/'.join(ret_url.split(" "))
    return redirect(url)

@app.route('/create/shablon', methods=["GET", "POST"])
def create_shablon():
    sf = ShablonForm()
    args=[]
    if (request.method=="POST"):
        shablons = os.listdir(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates")
        print(shablons)
        try:
            shablons.index(sf.name.data+".txt")
            args+=["exists"]
        except ValueError:
            args+=["OK"]
            open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+sf.name.data+".txt",'x')
    return render_template('create_shablon.html', form=sf, args=args)

@app.route('/choose/shablon/<string:name>/<string:ret_url>', methods=["GET", "POST"])
def choose_product_shablon(name, ret_url):
    cp = ChooseProduct()
    args=["shablon"]
    pm = ProductModel(db.get_connection())
    cm = CategoryModel(db.get_connection())
    if (request.method=="POST"):
        if (pm.exists(cp.select2.data)[0]):
            id_pr=int(pm.get_id(cp.select2.data)[0])
            file = open(os.getcwd()+slashes+'users'+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt", "r")
            s=""
            kek = True
            for line in file:
                product=line.strip().split()
                if (int(product[0])==id_pr):
                    kek = False
                item = pm.get(int(product[0]))
                if (len(item)>0):
                    s+=" ".join(product)+"\n"
            file.close()
            file = open(os.getcwd()+slashes+'users'+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt",'w')
            file.write(s)
            file.close()
            if (kek):
                args+=["OK"]
                file = open(os.getcwd()+slashes+'users'+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt", 'a')
                file.write(str(id_pr)+" 1\n")
                file.close()
            else:
                args+=["exists"]
            cp.select2.data=None
        else:
            args+=["choose_product"]
            products = cm.get_products(cm.get_id(cp.select1.data)[0])[0].split()
            productss=" "
            product=[]
            for i in products:
                item = pm.get(int(i))
                if (len(item)>0):
                    productss+=i+" "
                    product+=[item[1]]
            cm.update(cm.get_id(cp.select1.data)[0], products=productss)
            cp.select2.choices=product
            url = '/'.join(ret_url.split("|")[0].split(" "))+"/"+ret_url.split("|")[1]
            return render_template('choose_product.html',  args=args, url = url, form=cp, name_shablon=name)
    categories = cm.get_all()
    categories=[i[1] for i in categories]
    cp.select1.choices=categories
    args+=["choose_category"]
    url = '/'.join(ret_url.split("|")[0].split(" "))+"/"+ret_url.split("|")[1]
    return render_template('choose_product.html', args=args, url=url, form=cp, name_shablon=name)

@app.route('/reduce/shablon/<string:name>/<int:id>/<int:number>/<string:ret_url>', methods=["GET", "POST"])
def reduce_from_shablon(name, id, number, ret_url):
    file = open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt", 'r')
    s = ""
    pm = ProductModel(db.get_connection())
    for line in file:
        product=line.strip().split()
        if (int(product[0])==id):
            product[1] = int(product[1])-number
            if (product[1] > 0):
                product[1]=str(product[1])
                s+=" ".join(product)+"\n"
        else:
            item=pm.get(int(product[0]))
            if (len(item)>0):
                s+=" ".join(product)+"\n"
    file.close()
    file = open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt",'w')
    file.write(s)
    file.close()
    url = '/'.join(ret_url.split("|")[0].split(" "))+"/"+ret_url.split("|")[1]
    return redirect(url)

@app.route('/add/shablon/<string:name>/<int:id>/<int:number>/<string:ret_url>', methods=["GET","POST"])
def add_from_shablon(name, id, number, ret_url):
    file = open(os.getcwd() + slashes + "users" + slashes + session[
        'username'] + slashes + "favourite_templates" + slashes + name + ".txt", 'r')
    s = ""
    pm = ProductModel(db.get_connection())
    kek = True
    for line in file:
        product = line.strip().split()
        if (int(product[0]) == id):
            product[1] = int(product[1]) + number
            if (product[1] > 0):
                kek = False
                product[1] = str(product[1])
                s += " ".join(product) + "\n"
        else:
            item = pm.get(int(product[0]))
            if (len(item) > 0):
                s += " ".join(product) + "\n"
    file.close()
    file = open(os.getcwd() + slashes + "users" + slashes + session[
        'username'] + slashes + "favourite_templates" + slashes + name + ".txt", 'w')
    file.write(s)
    if (kek):
        file.write(str(id)+" "+str(number)+"\n")
    file.close()
    if (ret_url.find('|')!=-1):
        url = '/'.join(ret_url.split("|")[0].split(" ")) + "/" + ret_url.split("|")[1]
    else:
        url = '/'.join(ret_url.split(" "))
    return redirect(url)

@app.route('/delete/shablon/<string:name>/<int:id>/<string:ret_url>', methods=["GET", "POST"])
def delete_from_shablon(name, id, ret_url):
    file =open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt", 'r')
    s=""
    for line in file:
        item = line.strip().split()
        if (item[0]!=str(id)):
            s+=" ".join(item)+"\n"
    file.close()
    file =open(os.getcwd()+slashes+"users"+slashes+session['username']+slashes+"favourite_templates"+slashes+name+".txt", 'w')
    file.write(s)
    file.close()
    if (ret_url.find("|")!=-1):
        url = ret_url.split("|")
        url = "/".join(url[0].split(" "))+"/"+url[1]
    else:
        url = "/".join(ret_url.split(" "))
    return redirect(url)

@app.route('/add/busket/shablon/<string:name>/<string:ret_url>', methods=["GET", "POST"])
def add_busket_from_shablon(name, ret_url):
    file = open(os.getcwd()+slashes+"users" + slashes + session['username'] +slashes+"favourite_templates"+ slashes +name+".txt", 'r')
    s=""
    pm = ProductModel(db.get_connection())
    for line in file:
        product = line.strip().split()
        item = pm.get(int(product[0]))
        if (len(item)>0):
            print(item)
            s+=" ".join(product)+"\n"
            print(session['food'].keys())
            if (product[0] in session['food'].keys()):
                session['food'][product[0]] += int(product[1])
            else:
                session['food'][product[0]] = int(product[1])
            session.modified=True
            print(session['food'].keys())
    file.close()
    file = open(os.getcwd()+slashes+"users" + slashes + session['username'] +slashes+"favourite_templates"+ slashes +name+".txt",'w')
    file.write(s)
    file.close()
    print(session.items())
    url = "/".join(ret_url.split(" "))
    return redirect(url)

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
            session['username'] = lf.username.data
            session['rights'] = us.get_pole(username=lf.username.data, rights="")
            session['food'] = dict()
            session.modified=True
            return redirect('/profile')
        else:
            args += ["not_exists"]
    print(session.items())
    return render_template("login.html", form=lf, args=args)

@app.route('/add/busket/<int:id>/<int:number>/<string:ret_url>', methods=["GET", "POST"])
def add_busket(id, number, ret_url):
    if 'food' not in session.keys():
        session['food']=dict()
    if str(id) in session['food'].keys():
        session['food'][str(id)]+=number
    else:
        session['food'][str(id)]=number
    session.modified=True
    print(session['food'].keys())
    url = '/'.join(ret_url.split(" "))
    return  redirect(url)

@app.route('/reduce/busket/<int:id>/<int:number>/<string:ret_url>', methods=["GET", "POST"])
def reduce_busket(id, number, ret_url):
    if 'food' not in session.keys():
        session['food']=dict()
    if (str(id) in session['food'].keys()):
        session['food'][str(id)]-=number
        if (session['food'][str(id)]<=0):
            del  session['food'][str(id)]
    session.modified=True
    url = '/'.join(ret_url.split(" "))
    return redirect(url)

@app.route('/delete/busket/<int:id>/<string:ret_url>', methods=["GET", "POST"])
def delete_from_busket(id, ret_url):
    if 'food' not in session.keys():
        session['food']=dict()
    if str(id) in session['food'].keys():
        del session['food'][str(id)]
    session.modified=True
    url = '/'.join(ret_url.split(" "))
    return redirect(url)

@app.route('/show/busket', methods=["GET", "POST"])
def show_busket():
    if 'food' not in session.keys():
        session['food']=dict()
    busket = session['food']
    pm = ProductModel(db.get_connection())
    products = []
    summ = 0
    print(session['food'].keys())
    for key in busket.keys():
        product = pm.get(int(key))
        if (len(product)>0):
            products+=[[product[0], product[1], product[2], product[3], product[4], product[5], busket[key]]]
            if (str(datetime.date.today())>=product[4] and str(datetime.date.today())<=product[5]):
                summ+=product[3]*busket[key]
            else:
                summ+=product[2]*busket[key]
        else:
            del busket[key]
    session.modified=True
    url = " show busket"
    return render_template('work_with_buskets.html', products=products, time = str(datetime.date.today()), summ = summ, url=url)

@app.route('/show/sales', methods=["GET", "POST"])
def show_sales():
    list_sales = os.listdir(os.getcwd()+slashes+"sales")
    sales = []
    sm = ShopModel(db.get_connection())
    for sale in list_sales:
        i = 0
        file = open(os.getcwd()+slashes+"sales"+slashes+sale)
        av_sale = []
        for line in file:
            if (i==0):
                av_sale += [line.strip()]
            elif i==1:
                av_sale += line.strip().split()
            elif i==2:
                shops = line.strip().split()
                sh=[]
                for shop in shops:
                    item = sm.get(shop)
                    if (type(item).__name__!="NoneType"):
                        sh+=[item[1]]
                av_sale+=[[" ".join(sh)]]
            i+=1
        av_sale+=[i-3]
        file.close()
        sales+=[av_sale]
    return render_template('work_with_sales.html', sales=sales)

@app.route('/show/sale/<string:name_of_sale>', methods=["GET", "POST"])
def show_sale(name_of_sale):
    pm = ProductModel(db.get_connection())
    if (request.method=="POST"):
        file = open(os.getcwd() + slashes + "sales" + slashes + name_of_sale + ".txt", 'r')
        ch_product = dict()
        i = 0
        s=""
        for line in file:
            if (i>2):
                product = line.strip().split("|")
                if (type(pm.get(int(product[0]))).__name__!='NoneType'):
                    ch_product[product[0]]=float(product[1])
            else:
                s+=line
            i+=1

        for key in ch_product.keys():
            if (request.form[key]!=''):
                ch_product[key]=float(request.form[key])
        file.close()
        file = open(os.getcwd() + slashes + "sales" + slashes + name_of_sale + ".txt", 'w')
        file.write(s)
        for key in ch_product.keys():
            file.write(key+"|"+str(ch_product[key])+"\n")
        file.close()
    file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'r')
    i = 0
    products = []
    pm = ProductModel(db.get_connection())
    for line in file:
        if (i>2):
            product = line.strip().split("|")
            product[0]=int(product[0])
            pr = pm.get(product[0])
            if (type(pr).__name__!='NoneType'):
                products+=[[product[0], pr[1], product[1]]]
        i+=1
    file.close()
    url = " show sale "+name_of_sale
    return render_template('work_with_sale.html', products=products, name_of_sale=name_of_sale, url = url)

@app.route('/create/sale', methods=["GET", "POST"])
def create_sale():
    csf = CreateSaleForm()
    args=[]
    if (request.method=="POST"):
        sm = ShopModel(db.get_connection())
        date1 = request.form['start_of_sale']
        date2 = request.form['end_of_sale']
        date3 = str(datetime.date.today())
        if (date2 < date1):
            args+=["end < start"]
        if (date3 > date1):
            args+=["start < time"]
        if (date3 > date2):
            args+=["end < time"]
        sales = os.listdir(os.getcwd()+slashes+"sales")
        sales=[i[0:len(i)-4] for i in sales]
        try:
            sales.index(csf.name.data)
            args+=["exists"]
        except ValueError:
            if (args==[]):
                args+=["OK"]
                print(csf.places.data)
                file = open(os.getcwd()+slashes+"sales"+slashes+csf.name.data+".txt", 'x')
                places = []
                try:
                    csf.places.data.index('Все')
                    places =sm.get_all()
                    places = [str(i[0]) for i in places]
                except ValueError:
                    for place in csf.places.data:
                        places += [str(sm.get_id(place)[0])]
                file.write(csf.name.data+"\n"+date1+" "+date2+"\n"+" ".join(places)+"\n")
                file.close()
    sm = ShopModel(db.get_connection())
    shops = sm.get_all()
    shops = [i[1] for i in shops]
    shops+=["Все"]
    print(shops)
    csf.places.choices = shops
    return render_template('create_sale.html', form=csf, args=args)

@app.route('/delete/sale/<string:name_of_sale>', methods=["GET", "POST"])
def delete_sale(name_of_sale):
    os.remove(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt")
    return redirect('/show/sales')

@app.route('/choose/product/sale/<string:name_of_sale>/<string:ret_url>', methods = ["GET", "POST"])
def choose_product_to_sale(name_of_sale, ret_url):
    cp = ChooseProduct()
    pm = ProductModel(db.get_connection())
    args=["sale"]
    cm = CategoryModel(db.get_connection())
    ret_url = '/'.join(ret_url.split(" "))
    if (request.method=="POST"):
        if (pm.exists(cp.select2.data)[0]):
            file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'r')
            kek = True
            i = 0
            id_pr = pm.get_id(cp.select2.data)[0]
            print(id_pr)
            for line in file:
                if (i>2):
                    pr = line.strip().split("|")
                    if pr[0]==str(id_pr):
                        kek = False
                i+=1
            file.close()
            if (kek):
                args+=["OK"]
                product = pm.get(id_pr)
                file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'a')
                file.write(str(id_pr)+"|"+str(product[2])+"\n")
                file.close()
            else:
                args+=["exists"]
            cp.select2.data=None
        else:
            products =cm.get_products(cm.get_id(cp.select1.data)[0])[0].split()
            productss=" "
            pr = []
            for product in products:
                if (type(pm.get(int(product))).__name__!="NoneType"):
                    productss+=product+" "
                    item = pm.get(int(product))
                    pr+=[item[1]]
            pr.sort()
            cp.select2.choices=pr
            args+=["choose_product"]
            return render_template('choose_product.html', form = cp, args = args , url = ret_url, name_of_sale=name_of_sale)
    args+=["choose_category"]
    categories = cm.get_all()
    categories=[i[1] for i in categories]
    cp.select1.choices=categories
    return render_template('choose_product.html', name_of_sale=name_of_sale, form = cp, args=args, url = ret_url)

@app.route('/choose/category/sale/<string:name_of_sale>/<string:ret_url>', methods  = ["GET", "POST"])
def choose_category_to_sale(name_of_sale, ret_url):
    args = ["category"]
    cp = ChooseProduct()
    cm = CategoryModel(db.get_connection())
    pm = ProductModel(db.get_connection())
    name_of_category = ""
    if (request.method=="POST"):
        if (type(cm.get_id(cp.select1.data)).__name__!="NoneType"):
            products = cm.get_products(cm.get_id(cp.select1.data)[0])[0].split()
            productss=[]
            for product in products:
                if (type(pm.get(product)).__name__!="NoneType"):
                    productss+=[product]
            cm.update(id = cm.get_id(cp.select1.data)[0], products=" ".join(productss)+" ")
            products=productss
            name_of_category=cp.select1.data
            pr_dict = dict()
            for product in products:
                pr_dict[product]=0
            file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'r')
            i=0
            for line in file:
                if (i>2):
                    item = line.strip().split("|")
                    if item[0] in pr_dict.keys():
                        pr_dict[item[0]]=1
                i+=1
            file.close()
            file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'a')
            kek = False
            for product in pr_dict.keys():
                if (not pr_dict[product]):
                    pr = pm.get(int(product))
                    file.write(product+"|"+str(pr[2])+"\n")
                    kek = True
            if (kek):
                args+=["OK"]
            else:
                args+=["exists"]
            file.close()
    args+=["choose_category"]
    categories = cm.get_all()
    categories=[category[1] for category in categories]
    cp.select1.choices=categories
    url = '/'.join(ret_url.split(" "))
    return render_template('choose_product.html', args = args, form = cp, name_of_sale=name_of_sale, name_of_category=name_of_category, url = url)

@app.route('/delete/sale/<string:name_of_sale>/product/<int:id>/<string:ret_url>', methods=["GET", "POST"])
def delete_from_sale(name_of_sale, id, ret_url):
    i = 0
    s=""
    file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'r')
    for line in file:
        if (i>2):
            if (str(id)!=line.strip().split("|")[0]):
                s+=line
        else:
            s+=line
        i+=1
    file.close()
    file = open(os.getcwd()+slashes+"sales"+slashes+name_of_sale+".txt", 'w')
    file.write(s)
    file.close()
    url = '/'.join(ret_url.split(" "))
    return redirect(url)
@app.route('/exit')
def ex():
    if "username" in session.keys():
        del session['username']
    if "rights" in session.keys():
        del session['rights']
    if "food" in session.keys():
        del session['food']
    session.modified=True
    return redirect('/')


@app.route('/check/user/<string:username>/<string:password>', methods=['GET', 'POST'])
def check_user(username, password):
    um = UsersModel(db.get_connection())
    if (um.exists(username, password)[0]):
        return jsonify(answer="OK")
    else:
        return jsonify(answer="Problem")

@app.route('/android/get/categories')
def android_get_catrgories():
    cm = CategoryModel(db.get_connection())
    categories = cm.get_all()
    categories_numbers = [category[0] for category in categories]
    categories_names = [category[1] for category in categories]
    return jsonify(categories_names=json.dumps(categories_names), categories_numbers=json.dumps(categories_numbers))

@app.route('/android/get/product/<int:id>')
def android_get_product(id):
    pm = ProductModel(db.get_connection())
    product = pm.get(id)
    if (type(product).__name__=="NoneType"):
        return Response(status=404)
    else:
        print(product)
        return jsonify(id = json.dumps(product[0]), name = product[1], price = json.dumps(product[2]), sale = json.dumps(product[2]), is_sale = json.dumps((product[4]<=str(datetime.date.today()) and str(datetime.date.today())<=product[5])), image = product[6].split()[0])

@app.route('/android/get/shop/<int:id>')
def android_get_shop(id):
    sm = ShopModel(db.get_connection())
    shop = sm.get(id)

    if (type(shop).__name__!="NoneType"):
        images=os.listdir(os.getcwd() + slashes + 'static' + slashes + 'shops' + slashes + shop[1] + slashes + "img")
        return jsonify(images=images)
    else:
        return Response(status=404)

@app.route('/android/get/shop/picture/<int:id>/<string:name>')
def android_get_pictur(id, name):
    sm = ShopModel(db.get_connection())
    shop = sm.get(id)
    return send_file(os.getcwd()+slashes+'static'+slashes+"shops"+slashes+shop[1]+slashes+"img"+slashes+name)

@app.route('/android/get/product/shop/<int:id_sh>/product/<int:id>')
def get_product_from_shop(id_sh, id):
    pm = ProductModel(db.get_connection())
    product = pm.get(id)
    sm = ShopModel(db.get_connection())
    shop = sm.get(id_sh)
    db_shop = DB_SHOP(shop[1],slashes)
    shop_model=ProductShopModel(db_shop.get_connection())
    id_sh_product=shop_model.get_id(product[1])
    if (type(id_sh_product).__name__=="NoneType"):
        shop_model.insert(product[1],'',0, product[2], product[3], str(datetime.date(2018, 1, 1)), str(datetime.date(2018, 1, 1)))
    id_sh_product=shop_model.get_id(product[1])[0]
    sh_product = shop_model.get(id_sh_product)
    number = sh_product[3]
    image = product[6].split()[0]
    name = product[1]
    return jsonify(name = name, id = id_sh_product, image = image, number=number,price = sh_product[4], is_sale=((sh_product[6]<=str(datetime.date.today()) and str(datetime.date.today())<=sh_product[7])), sale = sh_product[5])

@app.route('/android/get/shops')
def android_get_shops():
    sm = ShopModel(db.get_connection())
    shops = sm.get_all()
    names = [shop[1] for shop in shops]
    ids = [shop[0] for shop in shops]
    return jsonify(names = names, ids = ids)

@app.route('/android/get/product/picture/<string:name>', methods=["GET"])
def android_get_picture_of_product(name):
    if (name.find('"')!=-1):
        name=name[0:name.find('"')]+name[name.find('"'):len(name)]
        if (name.find('"')!=-1):
            name=name[0:name.find('"')]+name[name.find('"'):len(name)]
    print(name)
    return send_file(os.getcwd()+slashes+'static'+slashes+'img'+slashes+name, mimetype="image/"+name[name.find('.')+1:len(name)])


@app.route('/android/search/<string:filter>/<string:value>', methods=['GET', 'POST'])
def android_search(filter, value):
    res = dict()
    sm = ShopModel(db.get_connection())
    shops = sm.get_all()
    shops = [[i[1], i[0]] for i in  shops]
    shops.sort()
    list_of_shablons=[]
    shablons_true=False
    if "username" in session.keys():
        shablons_true=True
        list_of_shablons = os.listdir(os.getcwd()+slashes+"users"+slashes+session['username'] +slashes+"favourite_templates")
        list_of_shablons=[i[0:len(i)-4] for i in list_of_shablons]

    if (filter=="category"):
        cm = CategoryModel(db.get_connection())
        name_of_category = cm.get(int(value))[1]
        pm = ProductModel(db.get_connection())
        ctm = CountryModel(db.get_connection())
        prm = ProducerModel(db.get_connection())
        products = cm.get_products(int(value))[0].split()
        ids=[]
        names=[]
        prices=[]
        is_sale=[]
        sales = []
        images=[]
        td = str(datetime.date.today())
        product=" "
        for i in products:
            item = pm.get(int(i))
            if (item!=None):
                product+=i+" "
                ids+=[item[0]]
                names+=[item[1]]
                prices+=[item[2]]
                if (item[4]<=td and td<=item[5]):
                    is_sale+=[True]
                else:
                    is_sale+=[False]
                sales+=[item[3]]
                images+=[item[6].split()[0]]

        ids = json.dumps(ids)
        names = json.dumps(names)
        prices = json.dumps(prices)
        is_sale = json.dumps(is_sale)
        sales = json.dumps(sales)
        images = json.dumps(images)
        return jsonify(ids = ids, names = names, prices = prices, is_sale = is_sale, sales = sales, images = images)
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
                av_shop = []
                for shop in shops:
                    db_shop = DB_SHOP(shop[0], slashes)
                    ProductShopModel(db_shop.get_connection()).init_table()
                    shop_model = ProductShopModel(db_shop.get_connection())
                    id_pr = shop_model.get_id(product[1])
                    if (type(id_pr).__name__ != "NoneType"):
                        av_shop += [shop]
                print([product[0], product[1], product[2], product[3], product[4], product[5],
                       product[6].split()[0], product[7], ctm.get(product[8])[1],
                       ctm.get_flag(product[8])[0], prm.get(product[9])[1], cm.get(product[10])[1], av_shop])
                product_items += [[product[0], product[1], product[2], product[3], product[4], product[5],
                                   product[6].split()[0], product[7], ctm.get(product[8])[1],
                                   ctm.get_flag(product[8])[0], prm.get(product[9])[1], cm.get(product[10])[1], av_shop]]
        product_result = [[product_items], (len(product_items)>0)]
        search_result = [category_result, producer_result, country_result, product_result]
        res["search_result"]=[search_result, search_result[0][1] or search_result[1][1] or search_result[2][1] or search_result[3][1]]
        print(res)
    url = " search "+str(filter)+" "+str(value)
    print(datetime.date.today())
    return jsonify(res)

@app.route('/android/get/locations/shop/<int:id>/product/<int:pr>')
def get_locations(id, pr):
    pm = ProductModel(db.get_connection())
    name_of_product = pm.get(pr)[1]
    sm = ShopModel(db.get_connection())
    name_of_shop = sm.get(id)[1]
    db_shop = DB_SHOP(name_of_shop, slashes)
    ProductShopModel(db.get_connection()).init_table()
    shop_product_model = ProductShopModel(db_shop.get_connection())
    id_product = shop_product_model.get_id(name_of_product)[0]
    product = shop_product_model.get(id_product)
    product_number = product[3]
    locations = product[2]
    if (locations!=''):
        pos_product=[]
        s = locations
        s = s[0:len(s) - 1]
        pos_products = [[int(i.split(':')[0]), [list(map(str, j.split("|"))) for j in i.split(':')[1].split()]] for i in
                        s.split('_')]
        poss=[]
        width = []
        for i in pos_products:
            kek=[]
            for j in i[1]:
                kek.append(int(j[0][0:len(j[0])-2]))
            poss.append([i[0],kek])
        width=poss
        kk = []
        for i in pos_products:
            kek=[]
            for j in i[1]:
                kek.append(int(j[1][0:len(j[1])-2]))
            kk.append([i[0],kek])
        height=kk
    else:
        locations=[]
        pos_products=[]
        kol = len(os.listdir(os.getcwd()+slashes+"static"+slashes+"shops"+slashes+sm.get(id)[1]+slashes+"img"))
        width=[]
        for i in range(kol):
            width.append([i,[]])
        height=[]
        for i in range(kol):
            height.append([i,[]])
    return jsonify(width = width, height=height)

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
