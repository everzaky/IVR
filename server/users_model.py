
class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_name VARCHAR(50),
                             email VARCHAR(128), 
                             password VARCHAR(128),
                             rights VARCHAR(50), 
                             favourite_products TEXT, 
                             ready_to_get_notifications_of_sales BOOLEAN,
                             ready_to_get_notifications_of_sales_of_favourite_products BOOLEAN
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, email, password, rights, favourite_products, ready_to_get_notifications_of_sales, ready_to_get_notifications_of_sales_of_favourite_products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, email, password, rights, favourite_products, ready_to_get_notifications_of_sales, ready_to_get_notifications_of_sales_of_favourite_products) 
                          VALUES (?,?,?,?, ?, ?, ?)''', (user_name, email, password, rights, favourite_products, ready_to_get_notifications_of_sales, ready_to_get_notifications_of_sales_of_favourite_products, ))
        cursor.close()
        self.connection.commit()

    def update(self, user_name, email=None, password=None, rights=None, favourite_products=None, ready_to_get_notifications_of_sales=None, ready_to_get_notifications_of_sales_of_favourite_products=None):
        cursor=self.connection.cursor()
        if (email != None):
            cursor.execute('''UPDATE users SET email = ? WHERE user_name = ?''', (email, user_name,))
        if (password != None):
            cursor.execute('''UPDATE users SET password = ? WHERE user_name = ?''', (password, user_name,))
        if (rights != None):
            cursor.execute('''UPDATE users SET rights = ? WHERE user_name = ?''', (rights, user_name,))
        if (favourite_products != None):
            cursor.execute('''UPDATE users SET favourite_products = ? WHERE user_name = ?''', (favourite_products, user_name,))
        if (ready_to_get_notifications_of_sales != None):
            cursor.execute('''UPDATE users SET ready_to_get_notifications_of_sales = ? WHERE user_name = ?''', (ready_to_get_notifications_of_sales, user_name,))
        if (ready_to_get_notifications_of_sales_of_favourite_products != None):
            cursor.execute('''UPDATE users SET ready_to_get_notifications_of_sales_of_favourite_products = ? WHERE user_name = ?''', (ready_to_get_notifications_of_sales_of_favourite_products, user_name,))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_pole(self, username, email=None, password=None, rights=None, favourite_products=None, ready_to_get_notifications_of_sales=None, ready_to_get_notifications_of_sales_of_favourite_products=None):
        cursor = self.connection.cursor()
        if (email!=None):
            cursor.execute('''SELECT email FROM users WHERE user_name = ?''', (username, ))
        if (password!=None):
            cursor.execute('''SELECT password FROM users WHERE user_name = ?''', (username, ))
        if (rights!=None):
            cursor.execute('''SELECT rights FROM users WHERE user_name = ?''', (username, ))
        if (favourite_products!=None):
            cursor.execute('''SELECT favourite_products FROM users WHERE user_name = ?''', (username, ))
        if (ready_to_get_notifications_of_sales!=None):
            cursor.execute('''SELECT ready_to_get_notifications_of_sales FROM users WHERE user_name = ?''', (username, ))
        if (ready_to_get_notifications_of_sales_of_favourite_products!=None):
            cursor.execute('''SELECT ready_to_get_notifications_of_sales_of_favourite_products FROM users WHERE user_name = ?''', (username,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (user_name, password,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def find(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get_email(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return row

    def get_user(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return row

    def find_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)