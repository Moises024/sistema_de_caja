import sqlite3
import os

class db():
    def __init__(self):
        self.conn=0
        
    def crearConnexion(self):
        try:
            path = os.path.join(os.path.abspath(""),"DB/Datos.db")
           
            con = sqlite3.connect(path)
            self.conn = con
        except sqlite3.Error as e:
            self.conn = e
            print(e)
        return self.conn
