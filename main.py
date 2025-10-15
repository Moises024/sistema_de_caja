from PyQt6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QMessageBox,QGraphicsOpacityEffect,QLabel,QWidget
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi 
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QCursor
import qasync
import asyncio
import sys
import math
import time 
import datetime
from component.login import conectar_acciones_login,conectar_botones_login,datos_usuarios
from component.caja import conectar_botones_caja,limpiar_lista,keys, back,vari,devuelta,click_ok_caja,buscador_articulos_input_caja
from component.almacen import  conectar_botones_almacen
from component.registrar import conectar_botones_registrar 
from component.inventario import conectar_botones_inventario
from component.cierre_caja import conectar_botones_cierre_caja,render_cierre_Caja,limpiar_lista as limpiar_cerrar_caja
from component.main_window import connectar_botones_main,activeLink,agregar_salir

from PyQt6.QtCore import Qt, QObject, QEvent, pyqtSignal


class msj():
    titulo =""
    text =""

def manejar_errores_task(futuro):
    try:
        futuro.result()
    except Exception as e:
        print(f"❌ Error en la tarea: {e}")
        # Aquí puedes mostrar un mensaje en la GUI si quieres

class TeclaListener(QObject):
   
     def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.key =""

     def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Period:
                    if self.parent.active: return True
                    self.parent.key_number = True 
                    self.parent.main_window.msg.setText("Números activados")
                    # animation(self,start,start_time,end,duration,obj,id):
                    iniciar = {
                         "start":int(self.parent.main_window.width() + self.parent.main_window.msg.width()),
                         "end":int(self.parent.main_window.width() - self.parent.main_window.msg.width()),
                         "duration":1000,
                         "obj": self.parent.main_window.msg,
                         "id":1
                    }
                    self.parent.animation(iniciar["start"],time.time()*1000,iniciar["end"],iniciar["duration"],iniciar["obj"],iniciar["id"])
                    self.parent.active =True
                if self.parent.caja.isVisible() and  self.parent.key_number:
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
                        
                         task =asyncio.create_task(datos_usuarios(self.parent.login,self.parent,self.parent.main_window))
                         task.add_done_callback(manejar_errores_task)
                    #    self.parent.userValidate( self.parent.login, self.parent.caja)
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
        self.tabla_column      = 5
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
        self.MAIN_WINDOW =10 
        self.timer = QTimer()
        self.animation_timer = QTimer()
        self.animation_timer_reverse = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.animation_timer.timeout.connect(self.move_all_animation)
        self.animation_timer_reverse.timeout.connect(self.move_all_animation_reverse)
        self.active = False
        self.btn_salir = None
        self.cliente_id=""
        self.copia_ =""
        self.connect_printer =False
        self.factura_detalle_id=""
        #pantalla clientes 
        self.ventana_cliente = loadUi("./ui/cliente.ui")
        self.ventana_cliente.btn_ok.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        #pantalla de Ventana Costo
        self.ventana_costo = loadUi("./ui/ventana_de_costo.ui")
        #pantalla actualizar_agatados 
        self.ventana_actualizar_agotados = loadUi("./ui/Actualizar_agotados.ui")
        #pantalla loading 
        self.loading = loadUi("./ui/loading.ui")
        #self.gif = QMovie("./img/loading.gif")
        
        
        #pantalla detalles 
        self.pantalla_detalles  = loadUi("./ui/PantallaDetalles.ui")
        self.pantalla_detalles.setWindowIcon(QIcon("./img/logo.png"))
        
       
        # venan cantidad
        self.ventana_cantidad = loadUi("./ui/IngresarCantidad.ui")
        
        # conectar btn ventana_cantidad
        
        self.ventana_cantidad.btn_ok.clicked.connect(lambda:click_ok_caja(self))
        
        # ventana producto agotado 
        self.producto_agotado = loadUi("./ui/ProductosAgotados.ui")

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
        caja = loadUi("./ui/Facturar.ui")
        self.almacen = loadUi("./ui/almacen.ui")
        self.caja = caja 
        
        #main Window 
        self.main_window = loadUi("./ui/mainWindow.ui")
       
        self.botones_main_window = [self.main_window.nav_1,self.main_window.nav_2,self.main_window.nav_3,self.main_window.nav_4]
        
        #cagar inventario 
        self.inventario = loadUi("./ui/inventario.ui")
        botones_inventario = [self.inventario.btn_inventario,self.inventario.btn_actualizar_factura,self.inventario.btn_eliminar_factura,self.pantalla_detalles.btn_detalle_actualizar,self.pantalla_detalles.btn_copia]
        conectar_botones_inventario(botones_inventario,self.inventario,self)

        #cagar regitsro ui
        self.registrar = loadUi("./ui/registrar.ui")
        botones_registrar = [self.registrar.btn_registrar]
        conectar_botones_registrar(botones_registrar,self.registrar,self)
        
        #cargar el ui
        login = loadUi("./ui/login.ui")
        self.login = login
        
        #cierre de caja 
        self.cierre_caja = loadUi("./ui/CierreDeCaja.ui")
        
        botones_cierre_caja  = [self.cierre_caja.btn_cerrar]
        
        buscador_articulos_input_caja(self)

        
        conectar_botones_cierre_caja(botones_cierre_caja,self)

               
        # Establecer la política de enfoque para que reciba eventos de teclado
       
        login.showFullScreen()  # Mostrar a pantalla completa
        login.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        login.setFocus()  # Establecer foco en el widget login
        login.contenedor.setFixedSize(login.width(),login.height())
        login.contenedor.move(0,0)
        login.input_nombre_usuario.setFocus()
        
        login.frame.move(math.floor(login.width()/2)-math.floor(login.frame.width()/2),math.floor(login.height()/2)-math.floor(login.frame.height()/2))
       
        self.animation(1000,time.time()*1000,login.frame_2.pos().x(),1000,login.frame_2,0)
        login.wallpaper.move(0,0)
        login.wallpaper.setFixedSize(login.width(),login.height())
       
       
        
        #Selección de los botones
        botones = [login.btn_acceder]
        
        #funciones de login 
        conectar_botones_login(botones,login,self,caja)
        conectar_acciones_login(login,self)

        #variables de caja
        botones_caja  = [caja.btn_cerrar_caja,caja.btn_0,caja.btn_00,caja.btn_1,caja.btn_2,caja.btn_3,caja.btn_4,caja.btn_5,caja.btn_6,caja.btn_7,caja.btn_8,caja.btn_9,caja.btn_valor_1,caja.btn_valor_2,caja.btn_valor_3,caja.btn_valor_4,caja.btn_borrar,caja.btn_igual,caja.btn_eliminar_lista,caja.generar_factura]
       

        #funciones de caja
        conectar_botones_caja(botones_caja,self,caja)
        

        #variables de almacen
        botones_almacen = [self.almacen.btn_agregar,self.almacen.btn_eliminar,self.almacen.btn_actualizar,self.almacen.btn_agotado,self.almacen.btn_calcular]
        

        #Funciones de almacen
        conectar_botones_almacen(botones_almacen, self )
       
        
        # Evento de cambio
        login.input_login.textChanged.connect(lambda: self.hide_password(login))
        self.current_window = login

        #Crear inputs a limpiar 
        self.inputs = [login.input_login,caja.monto_pagado,caja.precio_total,caja.input_buscar,caja.devuelta_2,caja.total]
    
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
               
                    
               if id == self.LOGIN_CODE:
                   self.tipo_msj.titulo ="Aviso"
                   self.tipo_msj.text ="¿Deseas cerrar sesión?"
                   res = self.sendMsjWarning(self.tipo_msj)
                   
                   if res == QMessageBox.StandardButton.Ok:
                        self.bandera = False
                        self.release = True
                        self.release_enter = True
                        self.clean_Window()
                        self.main_window.hide()
                        self.login.showFullScreen()
                        self.animation(1000,time.time()*1000,self.login.frame_2.pos().x(),1000,self.login.frame_2,0)
                        asyncio.create_task(activeLink(self,{"id":None}))
                        self.current_window = window  
                                            
                   else:
                       return 
               
               if id == self.CERRAR_SESION_CODE:
                       
                       limpiar_cerrar_caja(self)

                       self.clean_Window()
                       window.total_vendido.setText("")
                       self.tiempo_salida = datetime.datetime.now()
                       asyncio.create_task(render_cierre_Caja(self))
                       self.main_window.root.layout().addWidget(window)
                       window.setParent(self.main_window)
                       window.btn_cerrar.move(int(window.width()-window.btn_cerrar.width()),0)
                       window.move(int(self.main_window.width()/2)-int(window.width()/2),int(self.main_window.height()/2)-int(window.height()/2))
                       self.current_window = window


               self.clear_input(self.inputs)  
               self.password =""
               self.tecla["valor"] = ""

               if id == self.CAJA_CODE:
                    self.clean_Window()
                    self.main_window.root.layout().addWidget(window)
                    self.caja.setParent(self.main_window)
                    self.caja.move(0,self.main_window.header.height()-10)
                    self.caja.setFixedSize(self.main_window.width(),self.main_window.height())
                    self.caja.contenedor.move(int(self.caja.width()/2)-int(window.contenedor.width()/2),int(self.caja.height()/2) - int(window.contenedor.height()/2))
                    self.caja.contenedor.setStyleSheet("background-color:transparent;")

                    self.current_window =window
                    
               if id == self.INVENTARIO_CODE:
                     
                    window.msj_1.setText("")
                    window.msj_2.setText("")
                    window.msj_3.setText("")
                    window.ganancia_neta_text.setText("")
                    window.ganancia_neta.setText("")
                    self.clean_Window()
                    
                    self.inventario.setParent(self.main_window)
                    self.main_window.root.layout().addWidget(window)
                    self.inventario.contenedor.move(int(self.main_window.width()/2)-int(window.contenedor.width()/2),int(self.main_window.height()/2)-int(window.contenedor.height()/2))
                    self.current_window = window
                      

               if id == 7:
                    self.release_enter=True
               if self.REGISTRAR_CODE == id:
                    self.clean_Window()
                    window.input_nombre.setText("")
                    window.input_apellido.setText("")
                    window.input_contra.setText("")
                    window.input_usuario.setText("")
                    window.setParent(self.main_window)
                    self.main_window.root.layout().addWidget(window)
                    window.contenedor.move(int(self.main_window.width()/2)-int(window.contenedor.width()/2),int(self.main_window.height()/2)-int(window.contenedor.height()/2))

                    self.current_window = window
                    
               if id == self.ALMACEN_CODE:
                    
                    window.cantidad_articulo.setText("")
                    window.precio_articulo.setText("")
                    window.nombre_articulo.setText("")
                    window.costo.setText("")
                    self.clean_Window()
                    self.almacen.setParent(self.main_window)
                    self.main_window.root.layout().addWidget(window)
                    self.almacen.contenedor.move(int(self.main_window.width()/2)-int(window.contenedor.width()/2),int(self.main_window.height()/2)-int(window.contenedor.height()/2))
                    self.current_window = window
                    
                    # buscar_articulo(self)
                    # render_almacen(self)
               
               if id == self.MAIN_WINDOW:
                    
                    if self.usuario.rol == 3 and self.btn_salir == None:
                         agregar_salir(self.main_window,self)
                    
                    if self.usuario.rol != 3 and self.btn_salir:
                         self.btn_salir.setParent(None)
                         self.btn_salir.deleteLater()
                         self.btn_salir = None
                         
                    if self.usuario.rol != 3:
                              container_user = self.main_window.header.findChild(QWidget,"container_user",)
                              container_user.setFixedWidth(300)
                              salir = container_user.findChild(QWidget,"contenedor_btn_salir",) 
                              salir.move(container_user.width(),int(salir.height()/2))
                              user = container_user.findChild(QLabel,"user")
                              user.setFixedWidth(200)
                              user.setStyleSheet('''
                                   QLabel{
                                             color:#f1f1f1;
                                             font-size:18px;

                                        }
                              ''')                         
                    connectar_botones_main(self.botones_main_window,self)
                    self.current_window.hide()  
                  
                    self.loading.show()
                    # self.loading.loading.clear()
                    # self.loading.loading.setText("aparecer por favor")
                    # 
                    
                    window.showFullScreen()
                    window.msg.move(window.width(),window.header.height())

                    self.current_window =window
                    self.main_window.header.setFixedWidth(self.main_window.width())
                    self.main_window.root.setFixedSize(self.main_window.width(),self.main_window.height())
                    self.main_window.container_user.findChild(QLabel,"user").setText(self.usuario.nombre + " " + self.usuario.apellido )
                    asyncio.create_task(activeLink(self,{"id":0}))
                    self.loading.hide() 
                    

    #Función donde se simula el teclado
     def teclado(self,number,login): 
            input = login.input_login
            self.tecla["valor"] += str(number)
            input.setText(self.tecla["valor"])
     
     def clean_Window(self):
               self.current_window.setParent(None) 
               self.main_window.root.layout().removeWidget(self.current_window)
               self.current_window = None

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
     
     def animation(self,start,start_time,end,duration,obj,id):
          self.start = start
          self.end = end
          self.duration = duration
          self.obj = obj
          self.start_time = start_time
          if id == 0:
               self.timer.start(16)  # Aproximadamente 60 FPS
          if id == 1 :
               self.animation_timer.start(16)
          if id == -1:
               self.animation_timer_reverse.start(16)
         
     def update_animation(self):
          t = (int(time.time() * 1000) - self.start_time)/self.duration
          easy = self.esaseOut(t)
          effect = QGraphicsOpacityEffect()
          effect.setOpacity(easy)  # `easy` debe estar entre 0.0 (invisible) y 1.0 (opaco)

          if t >1: 
               t=1
               self.timer.stop()
               
          
          x = self.start + (self.end - self.start) * easy
          self.obj.move(int(x),self.obj.pos().y())
          self.obj.setGraphicsEffect(effect)
          
          
     def esaseOut(self,t):
          return 1-(1-t) * (1-t)

     def move_all_animation(self):

          t = (int(time.time() * 1000) - self.start_time)/self.duration
          easy = self.esaseOut(t)
          if t >= 1:
               self.animation_timer.stop()
               self.active =False
               asyncio.create_task(self.call_reverse())
               
               
          x = int(self.start + (self.end - self.start) * easy)

          self.obj.move(x,self.main_window.header.height())

     def move_all_animation_reverse(self):

          t = (int(time.time() * 1000) - self.start_time)/self.duration
          easy = self.esaseOut(t)
          if t >= 1:
               self.animation_timer_reverse.stop()
               self.active =False
               
          x = int(self.start + (self.end - self.start) * easy)
         
          self.obj.move(x,self.main_window.header.height())
     async def call_reverse(self):
          await asyncio.sleep(2)
          iniciar = {
                              "start":int(self.main_window.width() - self.main_window.msg.width()),
                              "end":int(self.main_window.width() + self.main_window.msg.width()),
                              "duration":2000,
                              "obj": self.main_window.msg,
                              "id":-1
                         }
               
          self.animation(iniciar["start"],time.time() *1000,iniciar["end"],iniciar["duration"],iniciar["obj"],iniciar["id"])
async def main():
     app = QApplication(sys.argv)
     ventana = Ventana()
     tecla_listener = TeclaListener(ventana)
     app.installEventFilter(tecla_listener)
     ventana.hide()

    # Corre el event loop de Qt con asyncio integrado
     await asyncio.Future()

class ClickableWidget(QWidget):
     clicked = pyqtSignal()
     def __init__(self,parent=None):
          super().__init__(parent)

     def mousePressEvent(self,event):
          self.clicked.emit()
          super().mousePressEvent(event)
     
if __name__ == "__main__":
   qasync.run(main())

