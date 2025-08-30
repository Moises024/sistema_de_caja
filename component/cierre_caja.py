from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView
from component.db import db
import sqlite3
import datetime
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
import aiohttp
import os
import json
import asyncio
from component.funciones import formatearDigitos


class Almacen:
    facturas=[]
    total_vendido=0
almacen = Almacen()

class Api:
    session=""
api =Api()

class Item:
    
    def __init__(self,no_factura,usuario,precio,fecha):
        self.no_factura = no_factura
        self.usuario = usuario
        self.precio = precio
        self.fecha = fecha
    
def conectar_botones_cierre_caja(botones,padre):
    botones[0].clicked.connect(lambda:padre.change_window(padre.login,padre.LOGIN_CODE))
    padre.cierre_caja.btn_cerrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


def render(padre,cantidad):
    padre.main_window.cargando.show()
    Item_ = QListWidgetItem()
    tabla = QTableWidget(cantidad,4)

    if padre.cierre_caja_cola:
        limpiar_lista(padre)
   
    tabla.setHorizontalHeaderLabels(["NO. FACTURA","USUARIO","TOTAL","FECHA"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight(padre.cierre_caja.list_caja.height())
    tabla.setRowCount(len(almacen.facturas))
    
    for i,factura in enumerate(almacen.facturas):
        index=0
        tabla.setItem(i,index,QTableWidgetItem(str(factura.no_factura)))
        tabla.setItem(i,index+1,QTableWidgetItem(str(factura.usuario)))
        tabla.setItem(i,index+2,QTableWidgetItem(formatearDigitos(str(factura.precio))))
        tabla.setItem(i,index+3,QTableWidgetItem(str(factura.fecha)))

    Item_.setSizeHint(tabla.sizeHint())
    padre.cierre_caja.list_caja.addItem(Item_)
    padre.cierre_caja.list_caja.setItemWidget(Item_,tabla)
    padre.cierre_caja_cola = Item_
    padre.cierre_caja.total_vendido.setText(formatearDigitos(str(almacen.total_vendido)))
    padre.main_window.cargando.hide()
    
async def render_cierre_Caja(padre):
    from component.main_window import cargando
    asyncio.create_task(cargando(padre))
    almacen.facturas = []
    almacen.total_vendido=0
    tiempo_inicio_str = datetime.datetime.strptime(str(padre.tiempo_inicio),'%Y-%m-%d %H:%M:%S.%f')
    tiempo_salida_str = datetime.datetime.strptime(str(padre.tiempo_salida),'%Y-%m-%d %H:%M:%S.%f')
    tiempo_inicio = int(tiempo_inicio_str.timestamp())
    tiempo_salida = int(tiempo_salida_str.timestamp())
    URL = os.getenv("URL") + "/api/inventario"
    if api.session !="":
        if not api.session.closed:
            await api.session.close()
    api.session = aiohttp.ClientSession()
    usuario = padre.usuario
    data = [tiempo_inicio,tiempo_salida,usuario._id] 
    headers = {
        "Content-Type":"Application/json",
        "id":"4"
    }
    try:
        async with api.session.post(URL,data= json.dumps(data),headers=headers) as resp:
        # cursor.execute("SELECT * FROM facturas JOIN usuarios ON usuarios.id = facturas.usuario_id  WHERE fecha >= ? and fecha <= ?",[tiempo_inicio,tiempo_salida])
            result = await resp.json()
            if not result["ok"]:
                return
            for factura in result["res"]:
                item = Item(factura["no_factura"],usuario.nombre + " " +  usuario.apellido,factura["total"],datetime.datetime.fromtimestamp(factura["fecha"]))
                almacen.total_vendido += int(factura["total"])
                almacen.facturas.append(item)
            render(padre,len(almacen.facturas))
           
    except sqlite3.Error as e:
        print(e)
        return

def limpiar_lista(padre): 
         # 1. Remover el widget visual
         if padre.cierre_caja_cola:
             
            padre.cierre_caja.list_caja.removeItemWidget(padre.cierre_caja_cola)  
            
            #    Eliminar el item de la lista para que no quede ocupando espacio
            fila =  padre.cierre_caja.list_caja.row(padre.cierre_caja_cola)
            padre.cierre_caja.list_caja.takeItem(fila)

