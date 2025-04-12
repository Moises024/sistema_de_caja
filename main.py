from PyQt6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.uic import loadUi 
import sys
import time

password = "1203"
class Error():
    titulo =""
    text =""

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.tecla = {"valor":""}
        self.msj = QMessageBox()
        self.layout_ = QVBoxLayout()
        
        #menu crea el l;a instancia del menu
        self.menuBar = self.menuBar()
        self.password =""
        
        #anade un menu
        archivo = self.menuBar.addMenu("Archivo")
        
        #crear los evento de la acccion
        salir_accion = QAction("Salir", self)
        
        #conectar el evento con una funcion
        salir_accion.triggered.connect(self.close)

        # Agrega la acción al menú
        archivo.addAction(salir_accion)
        
        caja = loadUi("./ui/caja.ui")
        
    
        #cargar el ui
        login = loadUi("./ui/login.ui")
        login.showFullScreen() 


        #activar los botones
        caja.actionSalir.triggered.connect(self.salir)
        caja.btn_cerrar.clicked.connect( lambda:self.change_window(login))

        login.btn_acceder.clicked.connect(lambda:self.userValidate(login,caja))
        login.salir.triggered.connect(self.salir)
        login.btn_borrar.clicked.connect(lambda:self.borrar(login))
        
        botones=[login.btn_0,login.btn_1,login.btn_2,login.btn_3,login.btn_4,login.btn_5,login.btn_6,login.btn_7,login.btn_8,login.btn_9]
       
        botones[0].clicked.connect(lambda:self.teclado(0,login)) 
        botones[1].clicked.connect(lambda:self.teclado(1,login)) 
        botones[2].clicked.connect(lambda:self.teclado(2,login)) 
        botones[3].clicked.connect(lambda:self.teclado(3,login)) 
        botones[4].clicked.connect(lambda:self.teclado(4,login)) 
        botones[5].clicked.connect(lambda:self.teclado(5,login)) 
        botones[6].clicked.connect(lambda:self.teclado(6,login)) 
        botones[7].clicked.connect(lambda:self.teclado(7,login)) 
        botones[8].clicked.connect(lambda:self.teclado(8,login))  
        botones[9].clicked.connect(lambda:self.teclado9(9,login)) 
        #label 
        tiempo = time.localtime()
        tiemp_locaL = time.strftime("%d-%m-%y    %H:%M:%S", tiempo)
        login.label_tiempo.setText(tiemp_locaL)

        
        # event change
        login.input_login.textChanged.connect(lambda:self.hide_password(login))
     
        self.current_window = login
    
    def salir(self):
        sys.exit()

        
    def userValidate(self,login,caja):
        valor =login.input_login.text()
        if valor == "":
            self.error.titulo ="Error"
            self.error.text = "Por favor escribe tu contraseña"
            self.sendMsjError(self.error)
            return
        if self.password == password:
            self.password =""
            self.tecla["valor"] =""
            login.input_login.setText("")
            self.change_window(caja)
            return
        
        self.error.titulo ="Error"
        self.error.text = "Contraseña incorrecta"
        self.sendMsjError(self.error)
        self.password=""
        self.tecla["valor"] =""
        login.input_login.setText("")
        login.input_login.setFocus()
        
    def hide_password(self,login):
        valor = login.input_login.text()  
        lista = list(valor)
        if lista:
            if lista[-1] != "*":
                self.password += lista[-1]
             
        nuevo_valor =""
        for string in lista:
            nuevo_valor += "*"
        login.input_login.setText(nuevo_valor)
         
    def sendMsjError(self,msj):
            self.msj.setText(msj.text)
            self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msj.setIcon(QMessageBox.Icon.Critical)
            self.msj.setWindowTitle(msj.titulo)
            self.msj.exec()
    
    def change_window(self,window):
            self.current_window.hide()
            window.showFullScreen() 
            self.current_window =window
    def teclado(self,number,login):
            input = login.input_login
            self.tecla["valor"] += str(number)
            input.setText(self.tecla["valor"])
    def borrar(self,login):
            input = login.input_login
            valor = input.text()
            new_valor_hide = valor[:-1]
            new_valor_password = self.password[:-1]
            self.password = new_valor_password
            self.tecla["valor"] = new_valor_password
            
            input.setText(new_valor_hide)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.hide()
    sys.exit(app.exec())