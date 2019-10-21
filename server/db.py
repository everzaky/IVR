import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("D:\\E1\\IVR\\server\\database.db", check_same_thread=False)
    def get_connection(self):
        return self.conn
    def __del__(self):
        self.conn.close()