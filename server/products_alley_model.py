class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products_alley
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name_of_product_alley VARCHAR(50),
                             products TEXT 
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_product_alley, products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products_alley
                        (name_of_product_alley, products) 
                          VALUES (?,?)
                        ''', (name_of_product_alley, products,))
        cursor.close()
        self.connection.commit()

    def update(self, id, name_of_product_alley = None, products = None):
        cursor =self.connection.cursor()
        if (name_of_product_alley!=None):
            cursor.execute('''UPDATE products_alley SET name_of_product_alley = ? WHERE id = ?''', (name_of_product_alley, id,))
        if (products!=None):
            cursor.execute('''UPDATE products_alley SET products = ? WHERE id =?''', (products, id,))
        cursor.close()
        self.connection.commit()

    def get_products(self, name_of_product_alley):
        cursor = self.connection.cursor()
        cursor.execute("SELECT products FROM products_alley WHERE name_of_product_alley = ?", (name_of_product_alley,))