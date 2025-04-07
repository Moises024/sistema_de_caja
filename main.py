from PyQt6.QtWidgets import QApplication,QMainWindow,QSizePolicy
from PyQt6 import uic 
import sys

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.login_label.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
    def msj(self,id):
        if id ==1:
            print("hola mundo")
        else:
            print(self.input_name.text())
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())