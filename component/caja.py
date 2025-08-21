from PyQt6.QtWidgets import QListWidgetItem,QTableWidgetItem,QTableWidget,QSizePolicy,QHeaderView,QLabel,QVBoxLayout,QWidget
from PyQt6.QtCore import Qt
from component.db import db
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCursor
from component.almacen import buscar_articulo
import sqlite3
import time
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
#convertir el label a aclickebel
class ClickLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
    def mousePressEvent(self,event):
        self.clicked.emit()
        super().mousePressEvent(event)

#Almacén de productos
class items:
    articulos=[]
    db_almacen = []
almacen = items()


class tecla:
   valor=""

class GlobalVaribles:
    item_global = ""
global_variable = GlobalVaribles()
keys = tecla()

#Clase para manejar variables globales del sistema de pagos
class varibles:
    render=False
    monto_total=0
    mont_pagado=0
    row_aliminada =""
    gen_factura = False
vari = varibles()

#Función para manejar la entrada del teclado
def teclado(caja):
    valor = caja.sender().text()
    if int(valor) >= 50:
      keys.valor = valor
    else:
        keys.valor += valor
    vari. mont_pagado = int(keys.valor)
    caja.monto_pagado.setText(keys.valor)

#Función para eliminar el último carácter del valor ingresado
def back(caja):
    keys.valor= keys.valor[:-1]
    caja.monto_pagado.setText(keys.valor)
    caja.devuelta_2.setText("")

#Alerta de cuando no se ingresa el pago
def devuelta(caja,padre):
   
   if caja.precio_total.text() == "" or caja.monto_pagado.text() == "" and not vari.render:
        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = f"No se puede hacer dicha operación"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        vari.render =False
        caja.devuelta_2.setText("")
        return
   vari.monto_total = 0
   vari.render = False

   #Calcula el monto total a cobrar
   for articulo in padre.articulos:
        vari.monto_total+= int(articulo["precio"])*int(articulo["cantidad"])
       
   vari.mont_pagado = int(vari.mont_pagado)
   keys.valor =""

   #Alerta de cuando ingresamos un pago menor que el total
   if vari.mont_pagado < vari.monto_total and not vari.render:
        msj = vari.monto_total - vari.mont_pagado
        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = f"Faltan {msj} pesos por cobrar"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        vari.render =False
        vari.monto_total=0
        caja.devuelta_2.setText("")
        return
   if  vari.monto_total ==0:
        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = f"no hay articulos en el carrito de compras"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        caja.devuelta_2.setText("")
        caja.monto_pagado.setText("")
        return
   
   #Calcula el monto a devolver
   monto_devolver = (vari.monto_total - vari.mont_pagado ) * -1

   vari.gen_factura = True

   if not vari.render:
        caja.devuelta_2.setText(str(monto_devolver))
        caja.monto_pagado.setText(str(vari.mont_pagado))
   else:
        caja.devuelta_2.setText("")
        caja.monto_pagado.setText("")

#Aparición de los productos en la lista
def buscar_item(caja,padre,item_buscado =False):
    tabla_pointer=0
    tabla_row =1
    informacion = caja.input_buscar.text()
    unidades=0
    item = QListWidgetItem()

    #Crea una tabla para mostrar los artículos
    tabla = QTableWidget(tabla_row,padre.tabla_column)
    tabla.resizeColumnsToContents()
    tabla.setHorizontalHeaderLabels(["Productos","Cant.","ITBIS","Precio"])
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Custom)
    tabla.setColumnWidth(0, 120)
    tabla.setColumnWidth(1, 60)
    tabla.setColumnWidth(2, 60)
    tabla.setColumnWidth(3, 100)
    
    tabla.setFixedHeight(caja.lista_articulo.height())
    tabla.verticalHeader().setVisible(False)
    tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    tabla.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tabla.setStyleSheet('''
        QHeaderView::section{
                        border:none;
                        border-bottom:3px solid #f1f1f1;
                        font-family:Dubai;
                        font-weight:bold;
                        color: rgb(107, 107, 107);
                        
                        }
        QTableWidget::item{
                        padding:10px;
                        border:none;
                        }
        QTableWidget::section::hover{
                        background-color:#232f42;
                        }
        QTableWidget::item::selected{
                        background-color:#232f42;
                        color:#f1f1f1;
                        border:none;
                        }
         QTableWidget::item::hover{
                        background-color:#232f4270;
                        color:#f1f1f1;
                        border:none;
                        }


''')
    bandera = False
    index=0
    total =0 
    numero_articulo =""
    cuenta_articulo =1

    #Buscar productos en el almacén
    if item_buscado == False:
        for item_dic in almacen.articulos:
        
            #Si se encuentra en el almacén lo mandará a la lista
            if item_dic["nombre"] == informacion or informacion == item_dic["ID"] or vari.render:
                if vari.render:
                    vari.row_aliminada =""
                    vari.render = False
                    if padre.cola_item_caja:
                        limpiar_lista(caja,padre)
                else:
                    id = is_already_exist(item_dic,padre)

                    if  id == "False":
                        padre.articulos.append(item_dic)
                        numero_articulo = id
                    else:
                        numero_articulo = id

                bandera =True
    else:
        bandera = True
        if len(item_buscado) > 1:

            numero_articulo = item_buscado[1]
        
    #Si no se encuentra no mandará nada       
    if not bandera:
        padre.tipo_msj.titulo ="Error"
        padre.tipo_msj.text = "Artículo no encontrado"
        padre.sendMsjError(padre.tipo_msj)
        return
    
    #Actualiza la tabla con los artículos encontrados
    for i,articulo in enumerate(padre.articulos):
        tabla.setRowCount(tabla_row)
        if numero_articulo == i:
            cuenta_articulo = int(articulo["cantidad"]) +1
            articulo["cantidad"] = cuenta_articulo
            tabla.setItem(numero_articulo,index,QTableWidgetItem(articulo["nombre"]))
            tabla.setItem(numero_articulo,index+1,QTableWidgetItem(f"x{articulo["cantidad"]}"))
           
            tabla.setItem(numero_articulo,index+2,QTableWidgetItem(f"0"))
            tabla.setItem(numero_articulo,index+3,QTableWidgetItem(f"{str(articulo["precio"])}"))
            
            unidades +=articulo["cantidad"]
        else:    
            
            tabla.setItem(tabla_pointer,index,QTableWidgetItem(articulo["nombre"]))
            tabla.setItem(tabla_pointer,index+1,QTableWidgetItem(f"x{articulo["cantidad"]}"))
            tabla.setItem(tabla_pointer,index+3,QTableWidgetItem(f"{str(articulo["precio"])}"))
            tabla.setItem(tabla_pointer,index+2,QTableWidgetItem(f"0"))
            unidades +=articulo["cantidad"]
        tabla_row +=1
        tabla_pointer+=1 
        index=0
        total += int(articulo["precio"])*int(articulo["cantidad"])
       
    tabla.cellClicked.connect(celda_click)
    caja.total.setText(str(total))
    padre.caja.detalles.findChild(QLabel,"unidades").setText(str(unidades))
    padre.inputs[2].setText(str(total))

    # Limpia la lista si hay artículos
    if(tabla_pointer >= 1 and padre.cola_item_caja):
        limpiar_lista(caja,padre)

    item.setSizeHint(tabla.sizeHint())
    caja.lista_articulo.addItem(item)
    caja.lista_articulo.setItemWidget(item,tabla)
    padre.cola_item_caja = item
    
#Eliminar productos de la lista
def eliminar_item(caja,padre):
    articulos = padre.articulos
    if vari.row_aliminada == "" or len(articulos) == 0:
            padre.tipo_msj.titulo ="Error"
            padre.tipo_msj.text = "El item no existe en la lista"
            padre.sendMsjError(padre.tipo_msj)
            return
    
    articulos[vari.row_aliminada]["cantidad"] = 1

    # if int(articulos[vari.row_aliminada]["cantidad"]) <=1:
    del articulos[vari.row_aliminada]

    caja.monto_pagado.setText("")

    caja.devuelta_2.setText("")
    

    # else:
    #     articulos[vari.row_aliminada]["cantidad"] = int(articulos[vari.row_aliminada]["cantidad"])-1
    vari.render =True
    buscar_item(caja,padre)
    

#Función para verificar si un artículo ya existe en la lista
def is_already_exist(item,padre):
    for i,articulo in enumerate(padre.articulos):
        if articulo["ID"] == item["ID"]: 
            return i
    return "False"

#Acciones de los botones
def conectar_botones_caja(botones,padre,caja):
 botones[0].clicked.connect( lambda:padre.change_window(padre.cierre_caja,padre.CERRAR_SESION_CODE))
 botones[1].clicked.connect(lambda:teclado(caja))
 botones[2].clicked.connect(lambda:teclado(caja))
 botones[3].clicked.connect(lambda:teclado(caja))
 botones[4].clicked.connect(lambda:teclado(caja))
 botones[5].clicked.connect(lambda:teclado(caja))
 botones[6].clicked.connect(lambda:teclado(caja))
 botones[7].clicked.connect(lambda:teclado(caja))
 botones[8].clicked.connect(lambda:teclado(caja))
 botones[9].clicked.connect(lambda:teclado(caja))
 botones[10].clicked.connect(lambda:teclado(caja))
 botones[11].clicked.connect(lambda:teclado(caja))
 botones[12].clicked.connect(lambda:teclado(caja))
 botones[13].clicked.connect(lambda:teclado(caja))
 botones[14].clicked.connect(lambda:teclado(caja))
 botones[15].clicked.connect(lambda:teclado(caja))
 botones[16].clicked.connect(lambda:back(caja))
 botones[17].clicked.connect(lambda:devuelta(caja,padre))
 botones[18].clicked.connect(lambda:eliminar_item(caja,padre))
 botones[19].clicked.connect(lambda:generar_facturas(padre))
 for boton in botones:
    boton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


def buscador_articulos_input_caja(padre):
    padre.caja.input_buscar.textChanged.connect(lambda text:sugerencia(text ,padre))
    
def conectar_acciones_caja(acciones,padre):
   
  
    acciones[0].triggered.connect(padre.salir)
    acciones[1].triggered.connect(lambda:padre.change_window(padre.almacen,padre.ALMACEN_CODE))
    acciones[2].triggered.connect(lambda:padre.change_window(padre.inventario,padre.INVENTARIO_CODE))
    acciones[3].triggered.connect(lambda:padre.change_window(padre.registrar,padre.REGISTRAR_CODE))

def limpiar_lista(caja,padre):
             # 1. Remover el widget visual
        if padre.cola_item_caja:
            caja.lista_articulo.removeItemWidget(padre.cola_item_caja)
    # 2. Eliminar el item de la lista para que no quede ocupando espacio
            fila = caja.lista_articulo.row(padre.cola_item_caja)
            caja.lista_articulo.takeItem(fila)
            


def celda_click(row,column):
    vari.row_aliminada = row

def buscar_articulos():
    #ID
    almacen.articulos = []
    almacen.db_almacen = []
    # baseDeDatos = db()
    # conn = baseDeDatos.crearConnexion()
    # cursor = conn.cursor()
    try:
        resp = requests.get(os.getenv("URL")+"/api/almacen")
        result = resp.json()
    
        for item in result['res']:
            
            almacen.db_almacen.append(item)
            almacen.articulos.append({"ID":item["id"],"nombre":item["nombre"],"cantidad":1,"precio":item["precio"]})
        # conn.close()
    except sqlite3.Error as err:
        print(err)
    
    

def generar_facturas(padre):
        if vari.gen_factura == False:
            padre.tipo_msj.titulo = "Warning"
            padre.tipo_msj.text = "No ha generado la devuelta"
            padre.sendMsjWarningSingle(padre.tipo_msj)
            return
        
        precio_total = int(vari.monto_total)
        fecha = int(time.time())
        usuario = padre.usuario
        
        factura= json.dumps(padre.articulos)
        # baseDeDatos = db()
        # conn = baseDeDatos.crearConnexion()
        # cursor = conn.cursor()
       
        try:
           
            for item in padre.articulos:
               
                for articulo in almacen.db_almacen:
                    if articulo["id"] == item["ID"]:
                         if int(articulo["cantidad"]) == 0:
                                padre.tipo_msj.titulo = "Error"
                                padre.tipo_msj.text = f"Ya no hay {item["nombre"]} en el almacén"
                                padre.sendMsjError(padre.tipo_msj)
                                return
                         if int(articulo["cantidad"]) < item["cantidad"]:
                                padre.tipo_msj.titulo = "Error"
                                padre.tipo_msj.text = f"No tienes suficientes {item["nombre"]} solo tienes  {articulo[2]} en el almacén"
                                padre.sendMsjError(padre.tipo_msj)
                                return
                             
                # cursor.execute("UPDATE articulos SET cantidad = cantidad - ? WHERE id =? and cantidad > 0 and cantidad >= ? ",(item["cantidad"],item["ID"],item["cantidad"]))
                # conn.commit()
                headers={
                    "Content-Type":"Application/json",
                    "id":"3"
                }
                data = []
                data.append(item["cantidad"])
                data.append(item["ID"])
                resp = requests.post(os.getenv("URL")+"/api/almacen",data=json.dumps(data),headers=headers)
                info = resp.json()
                if not info["ok"]:
                    #msj errior al cliente 
                    print(info["res"])
                    return
              
        except sqlite3.Error as err:
            print(err)
            return
        
        # cursor.execute("INSERT INTO facturas(usuario_id,factura,total,fecha) values(?,?,?,?)", (usuario.id, factura,precio_total, fecha))

        try:
            headers={
                    "Content-Type":"Application/json",
                    "id":"0"
                }
            data = []
        
            data.append(usuario.id)
            data.append(factura)
            data.append(precio_total)
            data.append(fecha)
            resp = requests.post(os.getenv("URL")+"/api/inventario",data=json.dumps(data),headers=headers)
            info = resp.json()
            if not info["ok"]:
                #msj erro al clienete 
                return
            buscar_articulo(padre)
            buscar_articulos()
            vari.render =False
            vari.mont_pagado=0
            vari.monto_total=0
            vari.gen_factura = False

            padre.tipo_msj.titulo = "Éxito"
            padre.tipo_msj.text = "Factura generada correctamente"
            padre.sendMsjSuccess(padre.tipo_msj)
            limpiar_completo(padre, padre.caja)
            buscar_articulos()
            padre.articulos =[]
            contenedor = QWidget()
            padre.caja.sugerencias.setWidget(contenedor)
            padre.caja.detalles.findChild(QLabel,"unidades").setText(str(0))
            # conn.commit()
        except sqlite3.Error as err:
            print(err)
            return
        
       
        # conn.close()
        
       

def limpiar_completo(padre, caja):
    limpiar_lista(caja, padre)
    caja.devuelta_2.setText("")
    caja.monto_pagado.setText("")
    caja.precio_total.setText("")
    caja.total.setText("")
    caja.input_buscar.setText("")
   

def sugerencia(texto,padre):

    contenedor = QWidget()
    if texto == "":
        padre.caja.sugerencias.setWidget(contenedor)
        return
    labels = QVBoxLayout(contenedor)
    labels_actions = []
    for item in almacen.articulos:
        
        if texto.lower() in item["nombre"].lower():
            label = ClickLabel(f"{item["nombre"]} : ID: {item["ID"]}")
            labels_actions.append([label,item])

    for label in labels_actions:
        labels.addWidget(label[0])
        connect_label(label,padre)
    padre.caja.sugerencias.setWidget(contenedor)
    padre.caja.sugerencias.findChild(QWidget).setStyleSheet('''
        QLabel{
                font-family:Dubai;
                padding-left:5px;
                color:#f1f1f1;
                font-size:18px;
                                                            }
        QLabel::hover{
                    background-color:#232f42;
                    color:#fff;                                           }
''')

    

def buscar_click(padre,item):
   
    global_variable.item_global = item

    if padre.ventana_cantidad.isVisible():
        padre.ventana_cantidad.hide()
        
    padre.ventana_cantidad.show()
    padre.ventana_cantidad.input_cantidad.setFocus()
    padre.key_number = False
   
   
def click_ok_caja(padre):
   
    valor = padre.ventana_cantidad.input_cantidad.text()
    if valor == '':
        return
    padre.ventana_cantidad.input_cantidad.setText("")
    cantidad =False 
    try:
        cantidad = int(valor)
    except:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Solo se permiten números"
        padre.sendMsjError(padre.tipo_msj)
        return

        
    global_variable.item_global["cantidad"] = cantidad
    bandera = False
    no_value = False
    if len(padre.articulos) == 0:
        
        padre.articulos.append(global_variable.item_global)
        no_value = True
    else: 
        for articulo in padre.articulos:
            if global_variable.item_global["ID"] == articulo["ID"]:
                    bandera = True
                   
            
    if bandera == False and no_value == False:
        padre.articulos.append(global_variable.item_global)    
    padre.ventana_cantidad.hide()
    buscar_item(padre.caja,padre,[global_variable.item_global])
    
def connect_label(label,padre):
    label[0].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    label[0].setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    label[0].setOpenExternalLinks(False)
    label[0].clicked.connect(lambda:buscar_click(padre,label[1]))
    
    
def actualizar_datos_caja():
    buscar_articulos()

    