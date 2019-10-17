class ProducerModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS producer
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     name_of_producer VARCHAR(50),
                                     products TEXT
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name_of_producer, products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO producer
                        (name_of_producer, products)
                        VALUES (?,  ?)
                        ''', (name_of_producer, products,))
        cursor.close()
        self.connection.commit()

    def exists(self, name_of_producer):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM producer WHERE name_of_producer = ?''', (name_of_producer,))
        row = cursor.fetchone()
        return (True,) if row else (False,)

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM producer WHERE id = ?''', (id,))
        cursor.close()
        self.connection.commit()

    def update(self,id, name_of_producer = None, products =None):
        cursor = self.connection.cursor()
        if (name_of_producer!=None):
            cursor.execute('''UPDATE producer SET name_of_producer = ? WHERE id = ?''',
                           (name_of_producer, id,))
        if (products!=None):
            cursor.execute('''UPDATE producer SET products = ? WHERE id = ?''', (products, id,))
        cursor.close()
        self.connection.commit()

    def get_products(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT products FROM producer WHERE id = ? ''', (id,))
        row = cursor.fetchone()
        return row

    def get_id(self, name_of_producer):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id FROM producer WHERE name_of_producer = ?''', (name_of_producer, ))
        row = cursor.fetchone()
        return row

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM producer WHERE id = ?''', (id,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM producer''')
        row = cursor.fetchall()
        return row