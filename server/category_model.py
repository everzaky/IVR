class CategoryModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS category
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name_of_category VARCHAR(50),
                             products TEXT 
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_category, products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO category
                        (name_of_category, products) 
                          VALUES (?,?)
                        ''', (name_of_category, products,))
        cursor.close()
        self.connection.commit()

    def update(self, id, name_of_category = None, products = None):
        cursor =self.connection.cursor()
        if (name_of_category!=None):
            cursor.execute('''UPDATE category SET name_of_category = ? WHERE id = ?''', (name_of_category, id,))
        if (products!=None):
            cursor.execute('''UPDATE category SET products = ? WHERE id =?''', (products, id,))
        cursor.close()
        self.connection.commit()

    def get_products(self, name_of_product_alley):
        cursor = self.connection.cursor()
        cursor.execute("SELECT products, id FROM category WHERE name_of_category  = ?", (name_of_product_alley,))
        row = cursor.fetchone()
        return row

    def exists(self, name_of_category):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM category WHERE name_of_category = ? ", (name_of_category,))
        row = cursor.fetchone()
        return True if row else False

    def  get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM category")
        row = cursor.fetchall()
        return row