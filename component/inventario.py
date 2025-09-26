from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView,QLabel,QWidget,QVBoxLayout,QFrame
from component.db import db
from PyQt6.QtGui import QCursor,QColor
from PyQt6.QtCore import Qt
import sqlite3
import datetime
import re
import requests
import os
import json
import aiohttp
from dotenv import load_dotenv
from component.funciones import formatearDigitos
import asyncio
load_dotenv()

class Api:
    session=""
api=Api()

class Almacen:
    facturas=[]
    eliminadas=None
    item = ""
almacen= Almacen()

class Item:
    def __init__(self,usuario,no_factura,total,fecha,usuario_id,detalles,costo):   
        self.usuario=usuario
        self.no_factura=no_factura
        self.total=total
        self.fecha=fecha  
        self.usuario_id = usuario_id  
        self.detalles = detalles
        self.costo = costo

def agrear_lista_elimar(row,c,padre):
    if c == 5 :
        if  padre.pantalla_detalles.isVisible():
            padre.pantalla_detalles.hide()
        detalles = json.loads(almacen.facturas[row].detalles)
        ventanita = QWidget()
       
        layout = QVBoxLayout(ventanita)

        padre.pantalla_detalles.no_factura.setText(str(almacen.facturas[row].no_factura))
        for detalle in detalles:
          
            label_1  = QLabel("Nombre: " +str(detalle["nombre"]))
            label_2  = QLabel("Cantidad: " +str(detalle["cantidad"]))
            label_3  = QLabel("Precio: " + formatearDigitos(str(detalle["total"])))
            linea = QFrame()
            linea.setFrameShape(QFrame.Shape.HLine)
            linea.setFrameShadow(QFrame.Shadow.Sunken)  # opcional
            linea.setStyleSheet("color: gray;")
            layout.addWidget(label_1)
            layout.addWidget(label_2)
            layout.addWidget(label_3)
            layout.addWidget(linea)
          
            
        padre.pantalla_detalles.detalles.setWidget(ventanita) 
        padre.pantalla_detalles.findChild(QWidget).setStyleSheet('''
        QLabel{
                font-family:Dubai;
                padding-left:5px;
                color:black;
                font-size:18px;
                                                            }
        QLabel::hover{
                    background-color:#232f42;
                    color:#fff;                                           }
''')
        
        #aqui
        padre.pantalla_detalles.show()
        return
    if almacen.item :
        almacen.eliminadas = almacen.item 
    else:
        almacen.eliminadas = row

def render_table(padre,cantidad,item=""):
    Item_ = QListWidgetItem()
    tabla = QTableWidget(cantidad,6)

    if padre.cola_item:
        limpiar_lista(padre)
    tabla.setHorizontalHeaderLabels(["USUARIO_ID","NO. ORDEN","USUARIO","TOTAL","FECHA","ACCION"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight( padre.inventario.tabla_factura.height())
    tabla.cellClicked.connect(lambda row ,c:agrear_lista_elimar(row,c,padre))
    tabla.setStyleSheet('''
    QScrollBar:vertical{
                background: #1e1e1e;
                width: 12px;
                margin: 0px 0px 0px 0px;      
                        }
''')
    tabla.verticalHeader().setVisible(False)
    #Si no hay un artículo específico, renderiza todos los artículos
    
    if item == "":
        tabla.setRowCount(len(almacen.facturas))
        agregar_Datos_tabla(tabla,almacen.facturas)
        
    else:
        tabla.setRowCount(len(item))
        agregar_Datos_tabla(tabla,item)
 

    Item_.setSizeHint(tabla.sizeHint())
    padre.inventario.tabla_factura.addItem(Item_)
    padre.inventario.tabla_factura.setItemWidget(Item_,tabla)
    padre.cola_item = Item_

async def eliminar(padre):
    
    if almacen.eliminadas == None:
       padre.tipo_msj.titulo = "Aviso"
       padre.tipo_msj.text = "Debe seleccionar una factura"
       padre.sendMsjWarning(padre.tipo_msj) #msj
       return
    
    item = ""
    if almacen.item:
       
        item = almacen.item
    else:
        item = almacen.facturas[almacen.eliminadas]
    
    #msj de que si esta seguro eliminar ese articulos
    no_factura = item.no_factura
    padre.tipo_msj.titulo = "Aviso"
    padre.tipo_msj.text = f"Seguro que quieres eliminar la factura con el NO. orden {no_factura}?"
    resp = padre.sendMsjWarning(padre.tipo_msj)
    
    if resp != 1024:
        return 
    if almacen.item:
        id = ""
        for i,iten in enumerate(almacen.facturas):
            if iten.no_factura == item.no_factura :
                id = i
        
        if await delete_de_baseDatos(almacen.facturas[id].no_factura,padre):
            del almacen.facturas[id]
    else:
        if await delete_de_baseDatos(almacen.facturas[almacen.eliminadas].no_factura,padre):
            del almacen.facturas[almacen.eliminadas]

    render_table(padre,len(almacen.facturas))
    almacen.eliminadas = None
    almacen.item = ""

def buscar_usuario(text,padre):
    if text == "":
        render_table(padre,len(almacen.facturas))
        return
    usuario= text

    nuevo_almacen = []
    isInt = isNumber(usuario)

    for item in almacen.facturas:
        if isInt:
            if int(usuario) == int(item.usuario_id):
                nuevo_almacen.append(item)
                almacen.item = item
        else:
            if re.search(usuario,item.usuario,re.IGNORECASE):
                nuevo_almacen.append(item)
                almacen.item = item

    if len(nuevo_almacen) == 0:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Usuario/id no encontrado"
        padre.sendMsjError(padre.tipo_msj)
        return
   
    render_table(padre,len(nuevo_almacen),nuevo_almacen)


def conectar_botones_inventario(botones,inventario,padre):
    botones[0].clicked.connect(lambda:hacer_inventario(padre))
    botones[1].clicked.connect(lambda:asyncio.create_task(buscar_facturas(padre)))
    botones[2].clicked.connect(lambda:asyncio.create_task(eliminar(padre)))
    inventario.input_factura.textChanged.connect(lambda text:buscar_usuario(text,padre))
    for btn in botones:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    padre.inventario.input_fecha_inicio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    padre.inventario.input_fecha_final.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

def isNumber(usuario):
    try:
        int(usuario)
        return True
    except:
        False

def hacer_inventario(padre): 
    mes = padre.inventario.input_fecha_inicio.text().strip()
    ano = padre.inventario.input_fecha_final.text().strip()
  
    try:
        fecha_inicio = datetime.datetime.strptime(mes,"%d/%m/%Y")
        fecha_final = datetime.datetime.strptime(ano,"%d/%m/%Y") 
    except:
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = "Debe agregar la fecha en este formato DD/MM/YYYY"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return 
        
    fecha_int_inicio = int(fecha_inicio.timestamp())
    fecha_int_final = int(fecha_final.timestamp()) + int(24*60*60)
    
    inventario =0
    ganancia = 0
    compra = 0

    for item in almacen.facturas:
        fecha_str = datetime.datetime.strptime(item.fecha,"%d/%m/%Y %H:%M:%S")
        fecha_int = int(fecha_str.timestamp())
        if fecha_int  >= fecha_int_inicio and fecha_int  <= fecha_int_final:
            inventario += int(item.total)
            facturas = json.loads(item.detalles)
            for factura_ in facturas:
                compra += int(int(factura_["costo"]) * int(factura_["cantidad"]))
   #Jump 
    ganancia = inventario - compra
   


    padre.inventario.msj_1.setText(f"El inventario desde el { mes}")
    padre.inventario.msj_2.setText(f"hasta el {ano} es de:")
    padre.inventario.msj_3.setText  (f"$" + formatearDigitos(str(inventario)))
    padre.inventario.ganancia_neta_text.setText("Ganancia Neta:")
    padre.inventario.ganancia_neta.setText(f" ${formatearDigitos(str(ganancia))}")
    
def limpiar_lista(padre): 
         # 1. Remover el widget visual
    padre.inventario.tabla_factura.removeItemWidget(padre.cola_item)  
    #    Eliminar el item de la lista para que no quede ocupando espacio
    fila =  padre.inventario.tabla_factura.row(padre.cola_item)
    padre.inventario.tabla_factura.takeItem(fila)

async def delete_de_baseDatos(id, padre):
    from component.main_window import cargando
    await cargando(padre)
    await asyncio.sleep(2)
    
    try:

        headers = {
            "Content-Type":"Application/json",
            "id":"1"
        }
        
        resp = requests.post(os.getenv("URL")+"/api/inventario",data=json.dumps({"_id":id}),headers=headers)
        data = resp.json()
        if not data["ok"]:

            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = data["res"]
            padre.sendMsjError(padre.tipo_msj)
            
            return False
        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = data["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        return True
    
    except sqlite3.Error as error:
        
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()


async def buscar_facturas(padre):
    from component.main_window import cargando
    await cargando(padre)
    facturas = []
    
    try:
        URL= os.getenv("URL")+"/api/inventario"
        if api.session!="":
            if not api.session.closed: 
                await api.session.close()
        api.session = aiohttp.ClientSession()
        async with api.session.get(URL) as resp:
             resultado = await resp.json()
             
             for fila in resultado["res"]:
                fecha = datetime.datetime.fromtimestamp(fila["fecha"])
                fecha_formateada = fecha.strftime('%d/%m/%Y %H:%M:%S')
                usuario_id = fila["usuario_id"]["id"]
                factura = Item(fila["usuario_id"]["nombre"] +" "+fila["usuario_id"]["apellido"], fila["no_factura"], fila["total"],fecha_formateada,usuario_id,fila["factura"],0)
                facturas.append(factura)
             almacen.facturas = facturas
             await api.session.close()
        padre.numero_orden =  len(almacen.facturas)
        render_table(padre,len(facturas))
        await api.session.close()
        padre.main_window.cargando.hide()
       
    except Exception  as e:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
        

def agregar_Datos_tabla(tabla,datos):
    for i,articulo in enumerate(datos):
            
            index=0
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.usuario_id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.no_factura)))
            tabla.setItem(i,index+2,QTableWidgetItem(str(articulo.usuario)))
            tabla.setItem(i,index+3,QTableWidgetItem(formatearDigitos(str(articulo.total))))
            tabla.setItem(i,index+4,QTableWidgetItem(str(articulo.fecha))) 
            tabla.setItem(i,index+5,QTableWidgetItem("ver")) 
            accion = tabla.item(i,index+5)
            accion.setForeground(QColor("white")) 
            accion.setBackground(QColor("#232f42"))
            accion.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
