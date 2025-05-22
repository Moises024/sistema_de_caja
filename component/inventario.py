from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView
from component.db import db
import datetime
import re


class Almacen:
    facturas=[]
    eliminadas=None
    item = ""
almacen= Almacen()

class Item:
    def __init__(self,usuario,no_factura,cantidad,fecha,usuario_id):   
        self.usuario=usuario
        self.no_factura=no_factura
        self.cantidad=cantidad
        self.fecha=fecha  
        self.usuario_id = usuario_id  

def agrear_lista_elimar(row,c):
    if almacen.item :
        almacen.eliminadas = almacen.item 
    else:
        almacen.eliminadas = row
    print(almacen.eliminadas)

def render_table(padre,cantidad,item=""):
    Item_ = QListWidgetItem()
    tabla = QTableWidget(cantidad,5)

    if padre.cola_item:
        limpiar_lista(padre)
    tabla.setHorizontalHeaderLabels(["USUARIO_ID","NO. ORDEN","USUARIO","CANTIDAD","FECHA"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight( padre.inventario.tabla_factura.height())
    tabla.cellClicked.connect(agrear_lista_elimar)

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

def eliminar(padre):
    print("eliminada: " ,almacen.eliminadas)
    if almacen.eliminadas == None:
       padre.tipo_msj.titulo = "Warning"
       padre.tipo_msj.text = "Debe seleccionar una factura"
       padre.sendMsjWarning(padre.tipo_msj) #msj
       return
    
    item = ""
    if almacen.item:
        print(almacen.item)
        item = almacen.item
    else:
        item = almacen.facturas[almacen.eliminadas]
    #msj de que si esta seguro eliminar ese articulos
    no_factura = item.no_factura
    padre.tipo_msj.titulo = "Warning"
    padre.tipo_msj.text = f"Seguro que quieres eliminar la factura con el NO. orden {no_factura}?"
    resp = padre.sendMsjWarning(padre.tipo_msj)
    if resp != 1024:
        return
    if almacen.item:
        id = ""
        for i,iten in enumerate(almacen.facturas):
            if iten.no_factura == item.no_factura :
                id = i
        del almacen.facturas[id]
    else:
        del almacen.facturas[almacen.eliminadas]
    render_table(padre,len(almacen.facturas))
    almacen.eliminadas = None
    almacen.item = ""

def buscar_usuario(inventario,padre):
    usuario= inventario.input_factura.text()
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
    botones[1].clicked.connect(lambda:buscar_usuario(inventario,padre))
    botones[2].clicked.connect(lambda:render_table(padre,len(almacen.facturas)))
    botones[3].clicked.connect(lambda:eliminar(padre))

    pass
def conectar_acciones_inventario(acciones, padre):
    acciones[0].triggered.connect(lambda:padre.change_window(padre.caja,1))
    acciones[1].triggered.connect(padre.salir)
def isNumber(usuario):
    try:
        int(usuario)
        return True
    except:
        False
def hacer_inventario(padre):
    mes = padre.inventario.input_fecha_inicio.text()
    ano = padre.inventario.input_fecha_final.text()
    
    fecha_inicio = datetime.datetime.strptime(mes,"%d/%m/%Y")
    fecha_final = datetime.datetime.strptime(ano,"%d/%m/%Y")
    fecha_int_inicio = int(fecha_inicio.timestamp())
    fecha_int_final = int(fecha_final.timestamp()) + int(24*60*60)
    print(fecha_int_inicio,fecha_int_final)
    inventario =0
    for item in almacen.facturas:
        fecha_str = datetime.datetime.strptime(item.fecha,"%d/%m/%Y %H:%M:%S")
        fecha_int = int(fecha_str.timestamp())
        if fecha_int  >= fecha_int_inicio and fecha_int  <= fecha_int_final:
            inventario += int(item.cantidad)

    padre.inventario.label_factura.setText(f"El inventario es desde { mes} hasta {ano} total : ${str(inventario)}")
def limpiar_lista(padre): 
         # 1. Remover el widget visual
    padre.inventario.tabla_factura.removeItemWidget(padre.cola_item)  
    #    Eliminar el item de la lista para que no quede ocupando espacio
    fila =  padre.inventario.tabla_factura.row(padre.cola_item)
    padre.inventario.tabla_factura.takeItem(fila)

def buscar_facturas(padre):
    database = db()
    conn = database.crearConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facturas JOIN usuarios ON usuarios.id = facturas.usuario_id order by facturas.fecha desc")
    facturas = []
    resultado = cursor.fetchall()
    for fila in resultado:
        time =  int(fila[4])
        fecha = datetime.datetime.fromtimestamp(time)
        fecha_formateada = fecha.strftime('%d/%m/%Y %H:%M:%S')
        usuario_id = fila[1]
        factura = Item(fila[6] +" "+fila[8], fila[0], fila[3],fecha_formateada,usuario_id)
        facturas.append(factura)
        almacen.facturas = facturas
    conn.close()
    padre.numero_orden =  len(almacen.facturas)
    render_table(padre,len(facturas))

    
    pass
def agregar_Datos_tabla(tabla,datos):
    for i,articulo in enumerate(datos):
            index=0
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.usuario_id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.no_factura)))
            tabla.setItem(i,index+2,QTableWidgetItem(str(articulo.usuario)))
            tabla.setItem(i,index+3,QTableWidgetItem(str(articulo.cantidad)))
            tabla.setItem(i,index+4,QTableWidgetItem(str(articulo.fecha))) 