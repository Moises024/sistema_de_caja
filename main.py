from PyQt6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QMessageBox
from PyQt6.QtGui import QAction,QIcon
from PyQt6.uic import loadUi 
from PyQt6.QtGui import QPixmap
from pathlib import Path
import sys
import math
import time
import datetime
from component.login import conectar_acciones_login,conectar_botones_login,datos_usurios
from component.caja import conectar_acciones_caja,conectar_botones_caja,limpiar_lista,keys, back,vari,devuelta,click_ok_caja,actualizar_datos_caja,buscador_articulos_input_caja
from component.almacen import conectar_acciones_almacen, conectar_botones_almacen,render_almacen
from component.registrar import conectar_acciones_registrar,conectar_botones_registrar
from component.inventario import conectar_botones_inventario,conectar_acciones_inventario,buscar_facturas
from component.cierre_caja import conectar_acciones_cierre_caja,conectar_botones_cierre_caja,render_cierre_Caja

from PyQt6.QtCore import Qt, QObject, QEvent



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
                
                if self.parent.caja.isVisible() and  self.parent.key_number :
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
                     if event.key() == Qt.Key.Key_Minus:
                          back(self.parent.caja)
                          return True
                     if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                          devuelta(self.parent.caja,self.parent)
                          return True
                     
                     
                if event.key() == Qt.Key.Key_Backspace and self.parent.release:
                   self.parent.tecla["key"] = "back"
                   self.parent.release= False

                if event.key() == Qt.Key.Key_Enter and self.parent.release_enter or event.key() == Qt.Key.Key_Return and self.parent.release_enter:
                
                    if self.parent.login.isVisible():
                        self.parent.release_enter = False
                        datos_usurios(self.parent.login,self.parent,self.parent.caja)
                    #     self.parent.userValidate( self.parent.login, self.parent.caja)
                        return True
     
            # Ejemplo: si presiona Enter
            
        return False  # False para dejar que el evento siga su curso



class Ventana(QMainWindow):
     def __init__(self):
        super().__init__()
        self.tipo_msj          = msj()
        self.tecla             = {"valor":"","key":""}
        self.msj               = QMessageBox()
        self.layout_           = QVBoxLayout()
        self.cola_item         = ""
        self.ventana_cantidad  = ""
        self.tabla_row         = 1
        self.bandera           = False
        self.release           = True
        self.release_enter     = True
        self.tabla_column      = 3
        self.tabla_pointer     = 0
        self.articulos         = []
        self.usuario           = ""
        self.key_number        = True
        self.cola_item_almacen = ""
        self.cola_item_caja    = False
        self.cierre_caja_cola  = False
        self.ventana_agotado_cola  = False
        self.numero_orden      = ""
        self.tiempo_inicio     = ""
        self.tiempo_salida     = "" 
        self.menu_caja         = False
        self.acciones_caja =[]
        self.popUp = []
        self.CAJA_CODE = 1
        self.ALMACEN_CODE = 8
        self.INVENTARIO_CODE= 4
        self.LOGIN_CODE = 0
        self.REGISTRAR_CODE = 5
        self.CERRAR_SESION_CODE = 6  
        
        
        # venan cantidad
        self.ventana_cantidad = loadUi("./ui/ventana_cantidad.ui")
        # conectar btn ventana_cantidad
        self.ventana_cantidad.btn_ok.clicked.connect(lambda:click_ok_caja(self))
        # ventana producto agotado 
        self.producto_agotado = loadUi("./ui/productos_agotados.ui")

        # Instalamos el filtro de eventos en la ventana principal
        self.popUp.append(self.producto_agotado)
        self.popUp.append(self.ventana_cantidad)
        
        #menu crea el l;a instancia del menu
        self.menuBar           = self.menuBar()
        self.password          = ""
        
        #anade un menu
        archivo                = self.menuBar.addMenu("Archivo")
        
        #crear los evento de la acccion
        salir_accion           = QAction("Salir", self)
        
        #conectar el evento con una funcion
        salir_accion.triggered.connect(self.close)

        # Agrega la acción al menú
        archivo.addAction(salir_accion)  
        caja = loadUi("./ui/caja.ui")
        self.almacen = loadUi("./ui/almacen.ui")
        self.caja = caja

        #cagar inventario 
        self.inventario = loadUi("./ui/inventario.ui")
        botones_inventario = [self.inventario.btn_inventario,self.inventario.btn_actualizar_factura,self.inventario.btn_eliminar_factura]
        conectar_botones_inventario(botones_inventario,self.inventario,self)
        acciones_inventario = [self.inventario.caja,self.inventario.salir]
        conectar_acciones_inventario(acciones_inventario,self)
        
        #cagar regitsro ui
        self.registrar = loadUi("./ui/registrar.ui")
        botones_registrar = [self.registrar.btn_registrar]
        conectar_acciones_registrar(self.registrar,self)
        conectar_botones_registrar(botones_registrar,self.registrar,self)
        #cargar el ui
        login = loadUi("./ui/login.ui")
        self.login = login
        
        #cierre de caja 
        self.cierre_caja = loadUi("./ui/cierre_caja.ui")
        
        botones_cierre_caja  = [self.cierre_caja.btn_cerrar]
        acciones_cierre_caja = [self.cierre_caja.actionCaja]
        buscador_articulos_input_caja(self)

        conectar_acciones_cierre_caja(acciones_cierre_caja,self)
        conectar_botones_cierre_caja(botones_cierre_caja,self)

               
        # Establecer la política de enfoque para que reciba eventos de teclado
       
        login.showFullScreen()  # Mostrar a pantalla completa
        login.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        login.setFocus()  # Establecer foco en el widget login
        login.contenedor.setFixedSize(login.width(),login.height())
        login.contenedor.move(0,0)
        
        login.frame.move(math.floor(login.width()/2)-math.floor(login.frame.width()/2),math.floor(login.height()/2)-math.floor(login.frame.height()/2))
     
        login.wallpaper.move(0,0)
        login.wallpaper.setFixedSize(login.width(),login.height())
       
       
        
        #Selección de los botones
        botones = [login.btn_acceder]
        
        #funciones de login 
        conectar_botones_login(botones,login,self,caja)
        conectar_acciones_login(login,self)

        #variables de caja
        botones_caja  = [caja.btn_cerrar_caja,caja.btn_0,caja.btn_00,caja.btn_000,caja.btn_1,caja.btn_2,caja.btn_3,caja.btn_4,caja.btn_5,caja.btn_6,caja.btn_7,caja.btn_8,caja.btn_9,caja.btn_valor_1,caja.btn_valor_2,caja.btn_valor_3,caja.btn_valor_4,caja.btn_valor_5,caja.btn_borrar,caja.btn_igual,caja.btn_eliminar_lista,caja.generar_factura]
       

        #funciones de caja
        conectar_botones_caja(botones_caja,self,caja)
        

        #variables de almacen
        botones_almacen = [self.almacen.btn_agregar,self.almacen.btn_eliminar,self.almacen.btn_actualizar,self.almacen.btn_agotado]
        acciones_almacen = [self.almacen.actionCaja,self.almacen.actionSalir]

        #Funciones de almacen
        conectar_botones_almacen(botones_almacen, self )
        conectar_acciones_almacen(acciones_almacen,self)
        
        # Evento de cambio
        login.input_login.textChanged.connect(lambda: self.hide_password(login))
        self.current_window = login

        #Crear inputs a limpiar 
        self.inputs =[login.input_login,caja.monto_pagado,caja.precio_total,caja.pago,caja.devuelta,caja.itbis,caja.input_buscar,caja.devuelta_2,caja.total]
    
    #Salir del sistema
     def salir(self):
        sys.exit()          
    
    #Alerta cuando deja el label vacio
    
        
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
            self.msj.setWindowIcon(QIcon("./img/logo.png"))
            return self.msj.exec()
             
     def sendMsjWarning(self,msj): 
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        self.msj.setIcon(QMessageBox.Icon.Warning)
        self.msj.setWindowTitle(msj.titulo)
        self.msj.setWindowIcon(QIcon("./img/logo.png"))
        res=self.msj.exec()
        return res 
    
     def sendMsjWarningSingle(self,msj): 
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msj.setIcon(QMessageBox.Icon.Warning)
        self.msj.setWindowTitle(msj.titulo)
        self.msj.setWindowIcon(QIcon("./img/logo.png"))
        res=self.msj.exec()
        return res 
    
     def sendMsjSuccess(self,msj): 
        self.msj.setText(msj.text)
        self.msj.setStandardButtons(QMessageBox.StandardButton.Ok)
        pixmap = QPixmap("./img/success.png")
        redimencionada = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.msj.setIconPixmap(redimencionada)
        self.msj.setWindowTitle(msj.titulo)
        self.msj.setWindowIcon(QIcon("./img/logo.png"))
        res=self.msj.exec()
        return res 
    
    #Función para cambiar de ventanas
     def change_window(self,window,id):
               self.cerrar_popUp()
               if id == self.CERRAR_SESION_CODE:
                   self.tipo_msj.titulo ="Warning"
                   self.tipo_msj.text ="¿Deseas cerrar sesión?"
                   res = self.sendMsjWarning(self.tipo_msj)
                   if res == QMessageBox.StandardButton.Ok:
                        self.bandera = False
                        self.release = True
                        self.release_enter = True
                        pass
                   else:
                       return 
               if id == 6 :
                       self.tiempo_salida = datetime.datetime.now()
                       render_cierre_Caja(self)

               self.clear_input(self.inputs)  
               self.current_window.hide()  
               window.showFullScreen() 
               self.current_window =window
               self.password =""
               self.tecla["valor"] = ""
               if id == self.CAJA_CODE:
                   
                    actualizar_datos_caja()
                    if self.usuario.rol == 3:
                       if self.menu_caja == False:
                            salir = QAction("Salir",self.caja)
                            inventario = QAction("Inventario",self.caja)
                            almacen = QAction("Almacén",self.caja)
                            registrar = QAction("Registrar",self.caja)
                            self.caja.menuArchivo.addAction(registrar)
                            self.caja.menuArchivo.addAction(inventario)
                            self.caja.menuArchivo.addAction(almacen)
                            self.caja.menuArchivo.addAction(salir)
                            self.acciones_caja.append(salir)
                            self.acciones_caja.append(almacen)
                            self.acciones_caja.append(inventario)
                            self.acciones_caja.append(registrar)
                            conectar_acciones_caja(self.acciones_caja,self)
                            self.menu_caja =True
                    else:

                       if self.menu_caja:
                            self.clearActions(self.caja.menuArchivo,self.acciones_caja)
                            self.menu_caja = False

                  
                    self.caja.nombre_usuario.setText(self.usuario.nombre + " " + self.usuario.apellido)
                    buscar_facturas(self)
                    self.caja.no_orden.setText(str(self.numero_orden+1))
               if id == self.INVENTARIO_CODE:
                    buscar_facturas(self)   

               if id == 7:
                    self.release_enter=True

               if id == self.ALMACEN_CODE:
                    render_almacen(self)

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
     def clearActions(self,menu,acciones):

          for accion in acciones:
               menu.removeAction(accion)
          self.acciones_caja = []
          
     def cerrar_popUp(self):
          for ventana in self.popUp:
               if ventana.isVisible():
                    ventana.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    tecla_listener = TeclaListener(ventana)
    app.installEventFilter(tecla_listener)
    ventana.hide()
    sys.exit(app.exec())
         

"""1- Poner las funciones a la ventana productos agotados
"""