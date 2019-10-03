
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
                             favourite_products TEXT
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, email, password, rights):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, email, password, rights) 
                          VALUES (?,?,?,?)''', (user_name, email, password, rights,))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
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

    def find_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        print(row)
        return (True, row[0]) if row else (False,)