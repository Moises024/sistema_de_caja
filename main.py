from PyQt6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QMessageBox,QTableWidget,QSizePolicy,QHeaderView
from PyQt6.QtGui import QAction
from PyQt6.uic import loadUi 
import sys
import time
from component.login import conectar_acciones_login,conectar_botones_login
from component.caja import conectar_acciones_caja,conectar_botones_caja,limpiar_lista,keys, back,vari,devuelta
from component.almacen import conectar_acciones_almacen, conectar_botones_almacen
from PyQt6.QtCore import Qt, QObject, QEvent

class variables():
    release_enter = True

var = variables()

class msj():
    titulo =""
    text =""

class TeclaListener(QObject):
   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.key =""
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
                
                if self.parent.caja.isVisible():
                     if event.key() == Qt.Key.Key_1:
                          keys.valor += "1"
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          vari.mont_pagado = int(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_2:
                          keys.valor += "2"
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          vari.mont_pagado = int(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_3:
                          keys.valor += "3"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_4:
                          keys.valor += "4"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_5:
                          keys.valor += "5"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_6:
                          keys.valor += "6"
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          vari.mont_pagado = int(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_7:
                          keys.valor += "7"
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          vari.mont_pagado = int(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_8:
                          keys.valor += "8"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_9:
                          keys.valor += "9"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_0:
                          keys.valor += "0"
                          vari.mont_pagado = int(keys.valor)
                          self.parent.caja.monto_pagado.setText(keys.valor)
                          return True
                     if event.key() == Qt.Key.Key_Backspace:
                          back(self.parent.caja)
                          return True
                     if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                          devuelta(self.parent.caja,self.parent)
                          return True
                     
                     
                if event.key() == Qt.Key.Key_Backspace and self.parent.release:
                   self.parent.tecla["key"] = "back"
                   self.parent.release= False

                if event.key() == Qt.Key.Key_Enter and var.release_enter or event.key() == Qt.Key.Key_Return and var.release_enter:
                
                    if self.parent.login.isVisible():
                        var.release_enter = False

                        self.parent.userValidate( self.parent.login, self.parent.caja)
                        return True
     
            # Ejemplo: si presiona Enter
            
        return False  # False para dejar que el evento siga su curso



class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tipo_msj = msj()
        self.tecla = {"valor":"","key":""}
        self.msj = QMessageBox()
        self.layout_ = QVBoxLayout()
        self.cola_item = ""
        self.tabla_row = 1
        self.bandera = False
        self.release = True
        self.tabla_column = 3
        self.tabla_pointer =0
        self.articulos = []
        self.usuario = {
             "nombre":"Moises Zabala",
             "pass":"1203"
        }
        # Creamos el listener
        

        # Instalamos el filtro de eventos en la ventana principal
        
        
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
        self.almacen = loadUi("./ui/almacen.ui")
        
        self.caja = caja
        
        #cargar el ui
        login = loadUi("./ui/login.ui")
        self.login = login
       
        # Establecer la política de enfoque para que reciba eventos de teclado
       
        login.showFullScreen()  # Mostrar a pantalla completa
        login.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        login.setFocus()  # Establecer foco en el widget login
       
        
        #Selección de los botones
        botones=[login.btn_0,login.btn_1,login.btn_2,login.btn_3,login.btn_4,login.btn_5,login.btn_6,login.btn_7,login.btn_8,login.btn_9,login.btn_acceder,login.btn_borrar]
        
        #funciones de login 
        conectar_botones_login(botones,login,self,caja)
        conectar_acciones_login(login,self)

        #variables de caja
        botones_caja =[caja.btn_cerrar,caja.btn_0,caja.btn_00,caja.btn_000,caja.btn_1,caja.btn_2,caja.btn_3,caja.btn_4,caja.btn_5,caja.btn_6,caja.btn_7,caja.btn_8,caja.btn_9,caja.btn_valor_1,caja.btn_valor_2,caja.btn_valor_3,caja.btn_valor_4,caja.btn_valor_5,caja.btn_borrar,caja.btn_igual,caja.btn_buscar,caja.btn_eliminar_lista]
        acciones_caja =[caja.actionSalir,caja.actionAlmacen]

        #funciones de caja
        conectar_botones_caja(botones_caja,self,login,caja)
        conectar_acciones_caja(acciones_caja,self)

        #variables de almacen
        botones_almacen = [self.almacen.btn_buscar,self.almacen.btn_agregar,self.almacen.btn_eliminar]
        acciones_almacen = [self.almacen.actionCaja,self.almacen.actionSalir]

        #Funciones de almacen
        conectar_botones_almacen(botones_almacen, self )
        conectar_acciones_almacen(acciones_almacen,self)
 
        #fecha y tiempo
        tiempo = time.localtime()
        tiemp_locaL = time.strftime("%d-%m-%y    %H:%M:%S", tiempo)
        login.label_tiempo.setText(tiemp_locaL)

        
        # Evento de cambio
        login.input_login.textChanged.connect(lambda: self.hide_password(login))
        self.current_window = login

        #Crear inputs a limpiar 
        self.inputs =[login.input_login,caja.monto_pagado,caja.precio_total,caja.pago,caja.devuelta,caja.itbis,caja.input_buscar,caja.devuelta_2,caja.total,caja.nombre_usuario,caja.no_orden]
    
    #Salir del sistema
    def salir(self):
        sys.exit()         
    
    #Alerta cuando deja el label vacio
    def userValidate(self,login,caja):
        caja.nombre_usuario.setText("")
        valor =login.input_login.text()

        if valor == "":
            self.tipo_msj.titulo ="Error"
            self.tipo_msj.text = "Por favor escribe tu contraseña"
            self.sendMsjError(self.tipo_msj)
            var.release_enter = True
            return
        
        if self.usuario["pass"] == self.password :
            self.password =""
            self.tecla["valor"] =""
            login.input_login.setText("")
            self.change_window(caja,1)
            caja.nombre_usuario.setText(self.usuario["nombre"])
            var.release_enter = True
            return
        
        #Alerta cuando la contraseña es incorrecta
        self.tipo_msj.titulo ="Error"
        self.tipo_msj.text = "Contraseña incorrecta"
        self.sendMsjError(self.tipo_msj)
        
        var.release_enter = True
        self.password=""
        self.tecla["valor"] =""
        login.input_login.setText("")
        login.input_login.setFocus()
        
    #Función para convertir la contraseña en asteriscos
    def hide_password(self,login):
        
        valor = login.input_login.text()   

        if self.bandera or valor == "": 
             self.bandera = False
             return
        lista = list(valor)
        if self.tecla["key"] == "back":
             self.borrar(login)
             self.release = True

             self.tecla["key"] =""
        if lista:
            if lista[-1] != "*":
                self.password += lista[-1]
        nuevo_valor =""

        for string in lista:
            nuevo_valor += "*"
        self.bandera = True
        login.input_login.setText(nuevo_valor)
        
    #Falta solucionar que cambie el estado de la tecla enter
    
    #Función para mandar las alertas de error
    def sendMsjError(self,msj):
            self.msj.setText(msj.text)
            self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msj.setIcon(QMessageBox.Icon.Critical)
            self.msj.setWindowTitle(msj.titulo)
            return self.msj.exec()
            
            
    def sendMsjWarning(self,msj): 
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        self.msj.setIcon(QMessageBox.Icon.Warning)
        self.msj.setWindowTitle(msj.titulo)
        res=self.msj.exec()
        return res 
    
    def sendMsjWarningSingle(self,msj): 
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
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
                if res == QMessageBox.StandardButton.Ok:
                     self.bandera = False
                     self.release = True
                     var.release_enter = True
                     pass
                else:
                    return 
            
            self.clear_input(self.inputs)  
            self.current_window.hide()  
            window.showFullScreen() 
            self.current_window =window
            self.password =""
            self.tecla["valor"] = ""

            
    
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
            
            self.bandera = True

            input.setText(new_valor_hide)

    def clear_input(self,inputs):
         for input in inputs:
              input.setText("")
         if self.cola_item :
            limpiar_lista(self.caja,self)
            self.articulos =[]
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    tecla_listener = TeclaListener(ventana)
    app.installEventFilter(tecla_listener)
    ventana.hide()
    sys.exit(app.exec())
         
         