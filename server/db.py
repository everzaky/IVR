import sqlite3
import os
class DB:
    def __init__(self, slaches):
        self.conn = sqlite3.connect(os.getcwd()+slaches + "database.db", check_same_thread=False)
    def get_connection(self):
        return self.conn
    def __del__(self):
        self.conn.close()