class ProductModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name_of_products VARCHAR(50),
                             price REAL ,
                             sale REAL ,
                             date_of_start TEXT,
                             date_of_end TEXT,
                             list_of_photos TEXT,
                             description TEXT, 
                             country INTEGER,
                             producer INTEGER,
                             category INTEGER                  
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_products, price, sale,  date_of_start, date_of_end, list_of_photos, description, country, producer, category):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products
                        (name_of_products, price, sale,  date_of_start, date_of_end, list_of_photos, description, country, producer, category)
                        VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?)''', (name_of_products, price, sale, date_of_start, date_of_end, list_of_photos,description,country,producer, category, ))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_products):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE name_of_products = ?''', (name_of_products,))
        row = cursor.fetchone()
        return (True, ) if row else (False,)

    def update(self,   id , name_of_products = None,  price = None, sale = None,  date_of_start = None, date_of_end=None, list_of_photos=None, description = None, country=None, producer=None, category = None):
        cursor = self.connection.cursor()
        if (name_of_products!=None):
            cursor.execute('''UPDATE products SET name_of_products WHERE  id = ?''', (name_of_products, id, ))
        if (price!=None):
            cursor.execute('''UPDATE products SET price = ? WHERE id = ?''', (price, id, ))
        if (sale!=None):
            cursor.execute('''UPDATE products SET sale = ? WHERE id = ?''', (sale, id,))
        if (date_of_start!=None):
            cursor.execute('''UPDATE products SET date_of_start = ? WHERE id = ?''', (date_of_start, id,))
        if (date_of_end!=None):
            cursor.execute('''UPDATE products SET date_of_end = ? WHERE id = ?''', (date_of_end, id,))
        if (list_of_photos!=None):
            cursor.execute('''UPDATE products SET list_of_photos = ? WHERE id = ?''',
                           (list_of_photos, id,))
        if (description!=None):
            cursor.execute('''UPDATE products SET description = ? WHERE id = ?''',
                           (description, id,))
        if (country!=None):
            cursor.execute('''UPDATE products SET country = ? WHERE id = ?''',
                           (country, id,))
        if (producer!=None):
            cursor.execute('''UPDATE products SET producer = ? WHERE id = ?''',
                           (producer, id,))
        if (category!=None):
            cursor.execute('''UPDATE products SET category = ? WHERE id = ?''', (category, id, ))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE id = ?''', (id,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products''')
        row = cursor.fetchall()
        return row

    def get_id(self, name_of_products):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id FROM products WHERE name_of_products = ?''', (name_of_products,))
        row = cursor.fetchone()
        return row

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE id = ?''', (id, ))
        cursor.close()
        self.connection.commit()
