from db import DB
from product_model import ProductModel
from shop_product_model import ProductShopModel
from shop_db import DB_SHOP
from shop_model import ShopModel
import time
import datetime
import platform
import os
slashes = ""

if platform.system() == "Windows":
    slashes = "\\"
else:
    slashes = "/"

db = DB(slashes)
ProductModel(db.get_connection())
pm = ProductModel(db.get_connection())
ShopModel(db.get_connection()).init_table()
sm = ShopModel(db.get_connection())
while (True):
    products = pm.get_all()
    for product in products:
        pm.update(id = product[0], date_of_start=str(datetime.date(2018,1,1)), date_of_end=str(datetime.date(2018, 1, 1)))
    sales = os.listdir(os.getcwd()+slashes+"sales")
    td = str(datetime.date.today())
    for sale in sales:
        kek = False
        i = 0
        file = open(os.getcwd()+slashes+"sales"+slashes+sale, 'r')
        for line in file:
            if (i==1):
                if (str(datetime.date.today())>line.strip().split(" ")[0]):
                    kek = True
                break
            i+=1
        file.close()
        if (kek):
            os.remove(os.getcwd()+slashes+"sales"+slashes+sale)
        else:
            file = open(os.getcwd()+slashes+"sales"+slashes+sale,'r')
            i = 0
            date_st = 0
            date_end = 0
            shops=[]
            for line in file:
                if (i==1):
                    date_st, date_end=line.strip().split(" ")
                elif (i==2):
                    shops = line.strip().split()
                    shopss = []
                    for shop in shops:
                        if (type(sm.get(int(shop))).__name__!="NoneType"):
                            shopss+=[shop]
                    shops = shopss
                elif i>2:
                    item = line.strip().split("|")
                    if (type(pm.get(int(item[0]))).__name__!="NoneType"):
                        product=pm.get(int(item[0]))
                        if (product[4]<=td and product[5]>=td):
                            if (product[2]<float(item[1])):
                                pm.update(id = int(item[0]), sale=float(item[1]), date_of_end=date_end, date_of_start=date_st)
                        else:
                            pm.update(id = int(item[0]), sale=float(item[1]), date_of_start=date_st, date_of_end=date_end)
                        for shop in shops:
                            db_shop=DB_SHOP(sm.get(shop)[1], slashes)
                            ProductShopModel(db_shop.get_connection())
                            shop_model = ProductShopModel(db_shop.get_connection())
                            if (type(shop_model.get_id(pm.get(item[0])[1])).__name__=='NoneType'):
                                shop_model.insert(name_of_product=product[1], date_of_end=str(datetime.date(2018, 1, 1)), date_of_start=str(datetime.date(2018, 1, 1)), location='', number_of_product=0, price=product[2], price_sale=product[3])
                            sh_product = shop_model.get(shop_model.get_id(product[1])[0])
                            if (sh_product[6]<=td and sh_product[7]>=td):
                                if (sh_product[5]<float(item[1])):
                                    shop_model.update(sh_product[0], price_sale=float(item[1]), date_of_start=date_st, date_of_end=date_end)
                            else:
                                shop_model.update(sh_product[0], price_sale=float(item[1]), date_of_start=date_st,
                                                  date_of_end=date_end)

                i+=1
            file.close()
    time.sleep(60)