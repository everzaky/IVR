class ProductShopModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shop
                                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                             name_of_product VARCHAR(50),
                                             location VARCHAR(50),
                                             number_of_product INTEGER 
                                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_product, location, number_of_product):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO shop
                        (name_of_product, location, number_of_product)
                        VALUES (?, ?, ?)''', (name_of_product, location, number_of_product))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_product):
        cursor  = self.connection.cursor()
        cursor.execute('''SELECT * FROM shop WHERE name_of_product = ?''', (name_of_product, ))
        row = cursor.fetchone()
        return (True, ) if row else (False,)


    def delete(self, name_of_product):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM shop WHERE name_of_product = ?''', (name_of_product, ))
        cursor.close()
        self.connection.commit()


