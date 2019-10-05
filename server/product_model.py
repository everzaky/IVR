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
                             date_of_start DATE,
                             date_of_end DATE,
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_products, price, sale, is_sale,  date_of_start, date_of_end):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products
                        (name_of_products, price, sale, is_sale, date_of_start, date_of_end)
                        VALUES (?, ?, ?, ?, ?, ?)''', (name_of_products, price, sale, is_sale, date_of_start, date_of_end, ))
        cursor.close()
        self.connection.commit()

    def update(self, name_of_products, price = None, sale = None, is_sale = None, date_of_start = None, date_of_end=None):
        cursor = self.connection.cursor()
        if (price!=None):
            cursor.execute('''UPDATE products SET price = ? WHERE name_of_products = ?''', (price, name_of_products, ))
        if (sale!=None):
            cursor.execute('''UPDATE products SET sale = ? WHERE name_of_products = ?''', (sale, name_of_products,))
        if (is_sale!=None):
            cursor.execute('''UPDATE products SET is_sale = ? WHERE name_of_products = ?''', (is_sale, name_of_products,))

