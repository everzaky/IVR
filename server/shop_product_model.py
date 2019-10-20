class ProductShopModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shop
                                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                             name_of_product TEXT,
                                             location TEXT,
                                             number_of_product INTEGER 
                                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_product, location, number_of_product):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO shop
                        (name_of_product, location, number_of_product)
                        VALUES (?, ?, ?)''', (name_of_product, location, number_of_product, ))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_product):
        cursor  = self.connection.cursor()
        cursor.execute('''SELECT * FROM shop WHERE name_of_product = ?''', (name_of_product, ))
        row = cursor.fetchone()
        return (True, ) if row else (False,)

    def get_id(self, name_of_product):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id FROM shop WHERE name_of_product = ?''', (name_of_product, ))
        row = cursor.fetchone()
        return row

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM shop WHERE id = ?''', (id, ))
        row = cursor.fetchone()
        return row

    def update(self, id,  name_of_product = None,  number_of_product = None, location = None):
        cursor = self.connection.cursor()
        if (name_of_product!=None):
            cursor.execute("""UPDATE shop SET name_of_product = ? WHERE id = ?""", (name_of_product, id, ))
        if (number_of_product!=None):
            cursor.execute('''UPDATE shop SET number_of_product = ? WHERE id = ?''', (number_of_product, id, ))
        if (location!=None):
            cursor.execute('''UPDATE shop SET location = ? WHERE id = ?''', (location, id, ))
        cursor.close()
        self.connection.commit()

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM shop WHERE id = ?''', (id, ))
        cursor.close()
        self.connection.commit()


