class ProductModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name_of_products VARCHAR(50),
                             price INTEGER,
                             sale INTEGER,
                             is_sale BOOLEAN,
                             date_of_start TEXT,
                             date_of_end TEXT,
                             list_of_photos TEXT,
                             description TEXT, 
                             country TEXT,
                             producer TEXT                   
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_products, price, sale, is_sale,  date_of_start, date_of_end, list_of_photos, description, country, producer):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products
                        (name_of_products, price, sale, is_sale, date_of_start, date_of_end, list_of_photos, description, country, producer)
                        VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?)''', (name_of_products, price, sale, is_sale, date_of_start, date_of_end, list_of_photos,description,country,producer, ))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_products):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE name_of_products = ?''', (name_of_products,))
        row = cursor.fetchone()
        return (True, ) if row else (False,)

    def update(self,  name_of_products, id = None, price = None, sale = None, is_sale = None, date_of_start = None, date_of_end=None, list_of_photos=None, description = None, country=None, producer=None):
        cursor = self.connection.cursor()
        if (price!=None):
            cursor.execute('''UPDATE products SET price = ? WHERE name_of_products = ?''', (price, name_of_products, ))
        if (sale!=None):
            cursor.execute('''UPDATE products SET sale = ? WHERE name_of_products = ?''', (sale, name_of_products,))
        if (is_sale!=None):
            cursor.execute('''UPDATE products SET is_sale = ? WHERE name_of_products = ?''', (is_sale, name_of_products,))
        if (date_of_start!=None):
            cursor.execute('''UPDATE products SET date_of_start = ? WHERE name_of_products = ?''', (date_of_start, name_of_products,))
        if (date_of_end!=None):
            cursor.execute('''UPDATE products SET date_of_end = ? WHERE name_of_products = ?''', (date_of_end, name_of_products,))
        if (list_of_photos!=None):
            cursor.execute('''UPDATE products SET list_of_photos = ? WHERE name_of_products = ?''',
                           (list_of_photos, name_of_products,))
        if (description!=None):
            cursor.execute('''UPDATE products SET description = ? WHERE name_of_products = ?''',
                           (description, name_of_products,))
        if (country!=None):
            cursor.execute('''UPDATE products SET country = ? WHERE name_of_products = ?''',
                           (country, name_of_products,))
        if (producer!=None):
            cursor.execute('''UPDATE products SET producer = ? WHERE name_of_products = ?''',
                           (producer, name_of_products,))
        cursor.close()
        self.connection.commit()

    def get(self, name_of_products):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE name_of_products = ?''', (name_of_products,))
        row = cursor.fetchone()
        return row

    def delete(self, name_of_products):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE name_of_products = ?''', (name_of_products, ))
        cursor.close()
        self.connection.commit()
