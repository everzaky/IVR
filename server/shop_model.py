class ShopModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shops
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     name_of_shop VARCHAR(50),
                                     location VARCHAR(50)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_shop, location):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO shops
                        (name_of_shop, location)
                        VALUES (?, ?)
                        ''', (name_of_shop, location,))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_shop):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM shops WHERE name_of_shop = ?''', (name_of_shop, ))
        row = cursor.fetchone()
        return (True,  ) if row else (False, )

    def delete(self, name_of_shop):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM shops WHERE name_of_shop = ?''', (name_of_shop, ))
        cursor.close()
        self.connection.commit()