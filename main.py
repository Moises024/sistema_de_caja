from PyQt6.QtWidgets import QApplication,QMainWindow,QSizePolicy
from PyQt6.uic import loadUi 
import sys

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = loadUi("./ui/login.ui", self)
        self.almacen = loadUi("./ui/almacen.ui")
        self.caja = loadUi("./ui/caja.ui")
        self.eliminar = loadUi("./ui/eliminar_articulo.ui")
        self.agregar = loadUi("./ui/agregar_articulo.ui")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())