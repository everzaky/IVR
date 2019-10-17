class CountryModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS country
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     name_of_country VARCHAR(50),
                                     flag VARCHAR(50),
                                     products TEXT
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_country, flag, products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO country
                        (name_of_country, flag, products)
                        VALUES (?, ?, ?)
                        ''', (name_of_country, flag,products, ))
        cursor.close()
        self.connection.commit()

    def get_id(self, name_of_country):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id FROM country WHERE name_of_country = ?''', (name_of_country, ))
        row = cursor.fetchone()
        return row

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM country WHERE id = ?''', (id, ))
        row = cursor.fetchone()
        return row

    def exists(self, name_of_country):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM country WHERE name_of_country = ?''', (name_of_country, ))
        row = cursor.fetchone()
        return (True,  ) if row else (False, )

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM country WHERE id = ?''', (id, ))
        cursor.close()
        self.connection.commit()

    def update(self, id, name_of_country = None, products = None):
        cursor = self.connection.cursor()
        if (name_of_country!=None):
            cursor.execute('''UPDATE country SET name_of_country = ? WHERE id = ?''', (name_of_country, id,))
        if (products!=None):
            cursor.execute('''UPDATE country SET products = ? WHERE id = ?''', (products, id,))
        cursor.close()
        self.connection.commit()

    def get_products(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT products FROM country WHERE id = ? ''', (id,))
        row = cursor.fetchone()
        return row

    def get_flag(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT flag FROM country WHERE id = ?''', (id,))
        row = cursor.fetchone()
        return row



    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM country''')
        row = cursor.fetchall()
        return row