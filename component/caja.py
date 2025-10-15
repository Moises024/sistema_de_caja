from PyQt6.QtWidgets import QListWidgetItem,QTableWidgetItem,QTableWidget,QSizePolicy,QHeaderView,QLabel,QVBoxLayout,QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCursor
import sqlite3
import time
import json
import requests
import os
import aiohttp
from dotenv import load_dotenv
import asyncio
from component.funciones import formatearDigitos
from component.printer import printer
import math
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
    clientes = []
almacen = items()

class Api:
    session =""
api= Api()


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
    devuelta=0
    recibido=0
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
    caja.monto_pagado.setText(formatearDigitos(keys.valor))

#Función para eliminar el último carácter del valor ingresado
def back(caja):
    keys.valor= keys.valor[:-1]
    caja.monto_pagado.setText(formatearDigitos(keys.valor))
    caja.devuelta_2.setText("")

#Alerta de cuando no se ingresa el pago
def devuelta(caja,padre):
   
   if caja.precio_total.text() == "" or caja.monto_pagado.text() == "" and not vari.render:
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = f"No se puede hacer dicha operación"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        vari.render =False
        caja.devuelta_2.setText("")
        return
   vari.monto_total = 0
   vari.render = False

   #Calcula el monto total a cobrar
   for articulo in padre.articulos:
        vari.monto_total+= int(articulo["total"])
       
   vari.mont_pagado = int(vari.mont_pagado)
   keys.valor =""

   #Alerta de cuando ingresamos un pago menor que el total
   if vari.mont_pagado < vari.monto_total and not vari.render:
        msj = vari.monto_total - vari.mont_pagado
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = f"Faltan {msj} pesos por cobrar"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        vari.render =False
        vari.monto_total=0
        vari.devuelta =0
        vari.recibido=0
        caja.devuelta_2.setText("")
        return
   
   if  vari.monto_total ==0:
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = f"no hay articulos en el carrito de compras"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        caja.devuelta_2.setText("")
        caja.monto_pagado.setText("")
        return
   
   #Calcula el monto a devolver
   monto_devolver = (vari.monto_total - vari.mont_pagado ) * -1
   vari.devuelta =monto_devolver
   vari.recibido= vari.mont_pagado
   vari.gen_factura = True

   if not vari.render:
        caja.devuelta_2.setText(formatearDigitos(str(monto_devolver)))
        caja.monto_pagado.setText(formatearDigitos(str(vari.mont_pagado)))
   else:
        caja.devuelta_2.setText("")
        caja.monto_pagado.setText("")

#Aparición de los productos en la lista
def buscar_item(caja,padre,item_buscado =False):
  
    tabla_row =1
    informacion = caja.input_buscar.text()
    item = QListWidgetItem()
 
    #Crea una tabla para mostrar los artículos
    tabla = QTableWidget(tabla_row,padre.tabla_column)
    tabla.resizeColumnsToContents()
    tabla.setHorizontalHeaderLabels(["Productos","Cant.","Precio","Descuento","Total"])
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Custom)
    tabla.setColumnWidth(0,int((20/100) * tabla.width()))
    tabla.setColumnWidth(1,int((8/100)  * tabla.width()))
    tabla.setColumnWidth(2,int((10/100) * tabla.width()))
    tabla.setColumnWidth(3,int((10/100) * tabla.width()))
    tabla.setColumnWidth(4,int((10/100) * tabla.width()))
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
                        background-color:#232f42
                        color:#f1f1f1;
                        border:none;
                        }


''')
    bandera = False
    numero_articulo =""
    #Buscar productos en el almacén
    if vari.render:
        bandera= True
        vari.row_aliminada =""
        vari.render = False
        if padre.cola_item_caja:
            limpiar_lista(caja,padre)

    if item_buscado == False:
        for item_dic in almacen.articulos:
        
            #Si se encuentra en el almacén lo mandará a la lista
            if item_dic["nombre"] == informacion or informacion == item_dic["ID"]:
              
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
    render_table(padre,tabla,numero_articulo,caja,item,tabla_row)

def render_table(padre,tabla,numero_articulo,caja,item,tabla_row):
    index=0
    total =0 
    cuenta_articulo =1
    unidades=0
    tabla_pointer=0
    
    for i,articulo in enumerate(padre.articulos):
        
        tabla.setRowCount(tabla_row)
        
        if numero_articulo == i:
            cuenta_articulo = int(articulo["cantidad"]) +1
            articulo["cantidad"] = cuenta_articulo
            tabla.setItem(numero_articulo,index,QTableWidgetItem(articulo["nombre"]))
            tabla.setItem(numero_articulo,index+1,QTableWidgetItem(f"x{articulo["cantidad"]}"))
            tabla.setItem(numero_articulo,index+2,QTableWidgetItem(f"{formatearDigitos(str(articulo["precio"]))}"))
            tabla.setItem(numero_articulo,index+3,QTableWidgetItem(f"{formatearDigitos(str(articulo["descuento"]))}"))
            tabla.setItem(numero_articulo,index+4,QTableWidgetItem(f"{formatearDigitos(str(articulo["total"]))}"))
            unidades +=articulo["cantidad"]
        
        else:    
            #JUMP 
            tabla.setItem(tabla_pointer,index,QTableWidgetItem(articulo["nombre"]))
            tabla.setItem(tabla_pointer,index+1,QTableWidgetItem(f"x{articulo["cantidad"]}"))
            tabla.setItem(tabla_pointer,index+2,QTableWidgetItem(f"{formatearDigitos(str(articulo["precio"]))}"))
            tabla.setItem(tabla_pointer,index+3,QTableWidgetItem(f"{formatearDigitos(str(articulo["descuento"]))}"))

            tabla.setItem(tabla_pointer,index+4,QTableWidgetItem(f"{formatearDigitos(str(articulo["total"]))}"))
            unidades +=articulo["cantidad"]
        tabla_row +=1
        tabla_pointer+=1 
        index=0
        total += int((articulo["total"]))
       
    tabla.cellClicked.connect(celda_click)
    caja.total.setText(formatearDigitos(str(total)))
    padre.caja.detalles.findChild(QLabel,"unidades").setText(str(unidades))
    padre.inputs[2].setText(formatearDigitos(str(total)))

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
    botones[19].clicked.connect(lambda:agregar_cliente(padre))
    padre.ventana_cliente.btn_ok.clicked.connect(lambda:asyncio.create_task(crearCliente(padre)))
    #aqui esta to asyncio.create_task(generar_facturas(padre))
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
   
    #ID
    # almacen.articulos = []
    # almacen.db_almacen = []
    # baseDeDatos = db()
    # conn = baseDeDatos.crearConnexion()
    # cursor = conn.cursor()

async def buscar_articulos(padre):
    URL = os.getenv("URL") + "/api/almacen"
    almacen.articulos = []
    almacen.db_almacen = []
    try:
        if api.session != "":
            if not api.session.closed:
                await api.session.close()
        api.session = aiohttp.ClientSession()
        
        async with api.session.get(URL) as resp:
            result = await resp.json()
            if not result['ok']:
                print(result['res'])
                return 
            
            for i,item in enumerate(result['res']):
              
                almacen.db_almacen.append(item)
                almacen.articulos.append({"ID":item["id"],"nombre":item["nombre"],"cantidad":1,"precio":item["precio"],"costo":item["costo"],"descuento":""})
            padre.main_window.cargando.hide()
            padre.caja.raise_()
            header={
                "Conten-Type":"Application/json",
                "id":"1"
            }
            api_ = requests.get(os.getenv("URL")+"/api/inventario",headers=header)
            resp = api_.json()
            if not resp["ok"]:
                return
            padre.caja.no_orden.setText(str(resp["res"])) 
            await buscar_clientes()
            
            # conn.close()
    except sqlite3.Error as err:
        print(err)
        padre.main_window.cargando.hide()
        padre.caja.raise_()

async def buscar_clientes():
    URL = os.getenv("URL") + "/api/cliente"

    try:
        if api.session != "":
            if not api.session.closed:
                await api.session.close()
        api.session = aiohttp.ClientSession()
        
        async with api.session.get(URL) as resp:
            result = await resp.json()
            if not result['ok']:
                print(result['res'])
                return 
        almacen.clientes = result['res']
        return almacen.clientes
    except Exception as e:
        print("error:" ,e, "Linea: 418 inevtario")
        pass
    
async def generar_facturas(padre,cliente):
       # jump

    
        padre.caja.repaint()  # fuerza el repintado
        padre.caja.lower()
        padre.main_window.cargando.show()
        await asyncio.sleep(0.5)
        
        if vari.gen_factura == False:
            padre.tipo_msj.titulo = "Aviso"
            padre.tipo_msj.text = "No ha generado la devuelta"
            padre.main_window.cargando.hide()
            padre.caja.raise_()
            padre.sendMsjWarningSingle(padre.tipo_msj)
            return
        
        precio_total = int(vari.monto_total)
        fecha = int(time.time())
        usuario = padre.usuario
        
        factura = padre.articulos[0:]
        print(cliente,"443")
        factura.append({"cliente_id":cliente["_id"]})
        factura= json.dumps(factura)
        # baseDeDatos = db()
        # conn = baseDeDatos.crearConnexion()
        # cursor = conn.cursor()
      
        try:
            
            for item in padre.articulos:
                            
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
                    padre.tipo_msj.titulo = "Error"
                    padre.tipo_msj.text = info["res"]
                    padre.sendMsjError(padre.tipo_msj)
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
        
            data.append(usuario._id)
            data.append(factura)
            data.append(precio_total)
            data.append(fecha)
            data.append(item["costo"])
            data.append(item["descuento"])
            data.append(vari.recibido)
            data.append(vari.devuelta)
            no_factura=0
            resp = requests.post(os.getenv("URL")+"/api/inventario",data=json.dumps(data),headers=headers)
            info = resp.json()
           
            if not info["ok"]:
                #msj erro al clienete 
                return
            no_factura = info["res"]
            vari.render =False
            vari.mont_pagado=0
            vari.monto_total=0
            vari.gen_factura = False
            padre.main_window.cargando.hide()
            padre.caja.raise_()
            padre.tipo_msj.titulo = "Éxito"
            
            padre.tipo_msj.text = "Factura generada correctamente"
            padre.sendMsjSuccess(padre.tipo_msj)
            
            padre.articulos =[]
            contenedor = QWidget()
            padre.caja.sugerencias.setWidget(contenedor)
            padre.caja.detalles.findChild(QLabel,"unidades").setText(str(0))
            asyncio.create_task(buscar_articulos(padre))
            data_factura ={
                "factura":factura,
                "total":precio_total,
                "devuelta":vari.devuelta,
                "recibido":vari.recibido,
                "no_factura":no_factura,
                "usuario":padre.usuario.nombre,
                "cliente":cliente["nombre"],
                "sector":cliente["sector"],
                "telefono":cliente['telefono']
            }
           
            limpiar_completo(padre, padre.caja)
            # conn.commit()
        except sqlite3.Error as err:
            print(err)
            padre.main_window.cargando.hide()
            padre.caja.raise_()
            return
        
       
        # conn.close()
        

def limpiar_completo(padre, caja):
    limpiar_lista(caja, padre)
    caja.devuelta_2.setText("")
    caja.monto_pagado.setText("")
    caja.precio_total.setText("")
    caja.total.setText("")
    caja.input_buscar.setText("")
    vari.monto_total=0
    vari.devuelta =0
    vari.recibido=0
    
   

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
    padre.ventana_cantidad.btn_ok.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    padre.ventana_cantidad.input_cantidad.setFocus()
    padre.key_number = False
   
   
def click_ok_caja(padre):
    is_pass=True
    items_almacen = ""
    valor = padre.ventana_cantidad.input_cantidad.text()
    descuento = padre.ventana_cantidad.input_descuento.text()

    
    if valor == '':
        return
    if descuento == "":
        descuento=0
    padre.ventana_cantidad.input_cantidad.setText("")
    padre.ventana_cantidad.input_descuento.setText("")
    cantidad =False 
    try:
        cantidad = int(valor)
        descuento = int(descuento)
    except:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Solo se permiten números"
        padre.sendMsjError(padre.tipo_msj)
        return
  
    for articulo in almacen.db_almacen:
        
        if global_variable.item_global["ID"] == articulo["id"]:
            items_almacen = articulo

            if int(articulo["cantidad"]) < cantidad:
                is_pass=False

    if not is_pass:
        #msj de que no tieni suficiente cantidad para agregar erl aryticulo
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = f"No tienes suficientes {items_almacen["nombre"]}, solo tienes {items_almacen["cantidad"]} en el almacén"
        padre.sendMsjError(padre.tipo_msj)
        return
    padre.key_number = True
    # descuento
    descuento = descuento
    
   
    item = ""
    item_ = ""
    bandera=True
    
    if len(padre.articulos) == 0:
        if descuento > 0 :
            descuentoAPlicado= math.floor((global_variable.item_global["precio"] * cantidad) - descuento)
            if descuentoAPlicado <= global_variable.item_global["costo"]:
                msj_rebaja(padre,devuelta)
                return
            #convierte el obj de string en un obj y esta copia el obj sin que sea el original solo un copia
            item_ = json.loads(json.dumps(global_variable.item_global))
            item_["total"] = descuentoAPlicado 
            item_["descuento"] = descuento
            item_["cantidad"] = cantidad
        else:
            item_ = global_variable.item_global  
            item_["total"] =  global_variable.item_global["precio"] * cantidad
            item_["descuento"] = descuento
            item_["cantidad"] = cantidad
    
    else: 
        item = global_variable.item_global
        item_= item
        articulo = exits_in(padre.articulos,item)
        if articulo:
            bandera =False
            if descuento > 0 :
                descuentoAPlicado= math.floor((articulo["precio"] * cantidad)- (articulo["descuento"] + descuento))
                if descuentoAPlicado <= articulo["costo"]:
                    msj_rebaja(padre,articulo["descuento"] + descuento)
                    return
                #usamos el obj original
                
                item_ = articulo
                item_["total"] = descuentoAPlicado 
                item_["descuento"] += descuento
                item_["cantidad"] += cantidad
            else:
                item_ = articulo 
                item_["total"] =  articulo["precio"]   * cantidad
                item_["descuento"] += descuento
                item_["cantidad"] += cantidad

        else:
            if descuento > 0 :
                    descuentoAPlicado= math.floor((global_variable.item_global["precio"]* cantidad)- descuento)
                    if descuentoAPlicado <= global_variable.item_global["costo"]:
                        msj_rebaja(padre,descuento)
                        return
                    item_["total"] =  descuentoAPlicado 
                    item_["cantidad"] = cantidad
                    item_["descuento"] = descuento
            else:
                
                item_["total"] =  global_variable.item_global["precio"] * cantidad
                item_["cantidad"] = cantidad
                item_["descuento"] = descuento
                       
    if bandera:
    
        padre.articulos.append(item_)  
  
    
    padre.ventana_cantidad.hide()
    buscar_item(padre.caja,padre,[item_])

   

def msj_rebaja(padre,descuento):
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "El sistema no te permite esta cantidad de descuento"
        padre.sendMsjError(padre.tipo_msj)
        padre.key_number = False
def connect_label(label,padre):
    label[0].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    label[0].setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    label[0].setOpenExternalLinks(False)
    label[0].clicked.connect(lambda:buscar_click(padre,label[1]))
    
    
    
def exits_in(array,item_):
    exist_ = False
    for item in array:
        if item["ID"] == item_["ID"]:
            exist_= item
    return exist_

def agregar_cliente(padre):
    padre.key_number = False
    if padre.ventana_cliente.isVisible():
        padre.ventana_cliente.hide()
    padre.ventana_cliente.show()


async def crearCliente(padre):
    URL = os.getenv("URL") + "/api/cliente"
    nombre = padre.ventana_cliente.input_cliente_nombre.text()
    telefono = padre.ventana_cliente.input_cliente_telefono.text()
    sector = padre.ventana_cliente.input_cliente_sector.text()
    id =""
    cliente = False
    for cliente_ in almacen.clientes:
        if cliente_["telefono"] == telefono:
            cliente = cliente_
    if nombre == "" or telefono == " ":
        # msj de error
        print("Debe rellenar los campos")
        return
    headers = {
        "Content-Type": "Application/json",
        "id":"0"
    }
    
    data = []
    data.append(nombre)
    data.append(telefono)
    data.append(sector)
    cliente
    padre.ventana_cliente.hide()

    

    if not cliente:
        cliente ={
            "nombre":nombre,
            "sector":sector,
            "telefono":telefono,
            "_id":""
        }
        try:
            if api.session != "":
                if not api.session.closed:
                    await api.session.close()
            api.session = aiohttp.ClientSession()

            async with api.session.post(URL,data=json.dumps(data),headers=headers) as resp:
                result = await resp.json()
                if not result['ok']:
                    print(result['res'])
                    return 
                id =  result['res']
                cliente["_id"] = id
                await generar_facturas(padre,cliente)        
        except Exception as e:
            print("error linea 785 de caja:" ,e)
            pass
    else:
        await generar_facturas(padre,cliente) 

    limpiar_completo(padre, padre.caja)
    limpiarcliente(padre)

def limpiarcliente(padre):
    padre.ventana_cliente.input_cliente_nombre.setText("")
    padre.ventana_cliente.input_cliente_telefono.setText("")
    padre.ventana_cliente.input_cliente_sector.setText("")