import sqlite3

class DB_SHOP:
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect("D:\\E1\\IVR\\server\\static\\shops\\"+name+"\\database.db", check_same_thread=False)
        print("D:\\E1\\IVR\\server\\static\\shops\\"+name+"\\database.db")

    def get_connection(self):
        return self.conn
    def __del__(self):
        self.conn.close()