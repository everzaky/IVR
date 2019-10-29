import sqlite3
import os

class DB_SHOP:
    def __init__(self, name, slaches):
        self.name = name
        self.conn = sqlite3.connect(os.getcwd()+slaches+"static"+slaches+"shops"+slaches+name+slaches+"database.db", check_same_thread=False)

    def get_connection(self):
        return self.conn
    def __del__(self):
        self.conn.close()