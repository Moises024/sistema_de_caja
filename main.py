from PyQt6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.uic import loadUi 
import sys
import time
from component.login import conectar_acciones_login,conectar_botones_login
from component.caja import conectar_acciones_caja,conectar_botones_caja

password = "1203"
class msj():
    titulo =""
    text =""

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tipo_msj = msj()
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

        #Selección de los botones
        botones=[login.btn_0,login.btn_1,login.btn_2,login.btn_3,login.btn_4,login.btn_5,login.btn_6,login.btn_7,login.btn_8,login.btn_9,login.btn_acceder,login.btn_borrar]
        
        #funciones de login 
        conectar_botones_login(botones,login,self,caja)
        conectar_acciones_login(login,self)

        #variables de caja
        botones_caja =[caja.btn_cerrar,caja.btn_0,caja.btn_00,caja.btn_000,caja.btn_1,caja.btn_2,caja.btn_3,caja.btn_4,caja.btn_5,caja.btn_6,caja.btn_7,caja.btn_8,caja.btn_9,caja.btn_valor_1,caja.btn_valor_2,caja.btn_valor_3,caja.btn_valor_4,caja.btn_valor_5,caja.btn_borrar,caja.btn_igual]
        acciones_caja =[caja.actionSalir]

        #funciones de caja
        conectar_botones_caja(botones_caja,self,login,caja)
        conectar_acciones_caja(acciones_caja,self)


        #fecha y tiempo
        tiempo = time.localtime()
        tiemp_locaL = time.strftime("%d-%m-%y    %H:%M:%S", tiempo)
        login.label_tiempo.setText(tiemp_locaL)

        
        # Evento de cambio
        login.input_login.textChanged.connect(lambda:self.hide_password(login))
        self.current_window = login
        #Crear inputs a limpiar 
        self.inputs =[login.input_login,caja.monto_pagado,caja.precio_total]
    
    #Salir del sistema
    def salir(self):
        sys.exit()

    #Alerta cuando deja el label vacio
    def userValidate(self,login,caja):
        valor =login.input_login.text()
        if valor == "":
            self.tipo_msj.titulo ="Error"
            self.tipo_msj.text = "Por favor escribe tu contraseña"
            self.sendMsjError(self.tipo_msj)
            return
        
        if self.password == password:
            self.password =""
            self.tecla["valor"] =""
            login.input_login.setText("")
            self.change_window(caja,1)
            return
        
        #Alerta cuando la contraseña es incorrecta
        self.tipo_msj.titulo ="Error"
        self.tipo_msj.text = "Contraseña incorrecta"
        self.sendMsjError(self.tipo_msj)
        self.password=""
        self.tecla["valor"] =""
        login.input_login.setText("")
        login.input_login.setFocus()
        
    #Función para convertir la contraseña en asteriscos
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
    
    #Función para mandar las alertas de error
    def sendMsjError(self,msj):
            self.msj.setText(msj.text)
            self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msj.setIcon(QMessageBox.Icon.Critical)
            self.msj.setWindowTitle(msj.titulo)
            self.msj.exec()
            
    def sendMsjWarning(self,msj):
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        self.msj.setIcon(QMessageBox.Icon.Warning)
        self.msj.setWindowTitle(msj.titulo)
        res=self.msj.exec()
        return res 
         
    #Función para cambiar de ventanas
    def change_window(self,window,id):
            if id == 0:
                self.tipo_msj.titulo ="Warning"
                self.tipo_msj.text ="¿Deseas cerrar sesión?"
                res = self.sendMsjWarning(self.tipo_msj)
                if res == QMessageBox.StandardButton.Ok :
                     pass
                else:
                    return 
            self.clear_input(self.inputs)  
            self.inputs[2].setText("1000")
            self.current_window.hide()  
            window.showFullScreen() 
            self.current_window =window
    
    #Función donde se simula el teclado
    def teclado(self,number,login):
            input = login.input_login
            self.tecla["valor"] += str(number)
            input.setText(self.tecla["valor"])


    #Función del boton para eliminar caracteres
    def borrar(self,login):
            input = login.input_login
            valor = input.text()
            new_valor_hide = valor[:-1]
            new_valor_password = self.password[:-1]
            self.password = new_valor_password
            self.tecla["valor"] = new_valor_password
            
            input.setText(new_valor_hide)
    def clear_input(self,inputs):
         for input in inputs:
              input.setText("")
         
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.hide()
    sys.exit(app.exec())