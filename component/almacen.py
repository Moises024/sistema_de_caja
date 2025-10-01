from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import Qt
import threading
import requests
import aiohttp
import os
from qasync import asyncSlot
from dotenv import load_dotenv
import json
import asyncio
from PyQt6.QtGui import QCursor,QColor
from component.funciones import formatearDigitos

load_dotenv()

class Thread_:
    Hilos=[]
    stop_event = threading.Event()
thread_ = Thread_()

class contenedorArticulo:
    articulos=[]
    item=""
    eliminadas=""
    agotado = []
almacen = contenedorArticulo()

class Api:
    session=""
api = Api()
class Variable:
    mi_funcion = ''
    mi_funcion_on=False
variable = Variable()
#Clase para representar un artículo
class item:
    
    def __init__(self,nombre,precio,cantidad,costo,id=""):
        self.id =id 
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.costo = costo


#Función para verificar si un valor es un entero    
def isInt(valor):
    try:
        int(valor)
        return True
    except:
        return False

#Función para buscar un artículo en el inventario        
def buscar(text,padre):
       
    if text == "":
        almacen.item = ""
        render_table(padre,len(almacen.articulos))
     
        return
    id = False
    nombre = text
    items_ =[]
    bandera = False

    if isInt(text): 
        id = int(text)
    
    #Busca el artículo en la lista de artículos
    for articulo in almacen.articulos:
        
        if  id == False:
            
            if nombre.lower() in articulo.nombre.lower():
                items_.append(articulo) 
                bandera=True
        else:
            if id == int(articulo.id):
                items_.append(articulo) 
                bandera=True

    #Si no se encontró el artículo
    if not bandera:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Artículo no encontrado"
        padre.sendMsjError(padre.tipo_msj)
        return
    almacen.item = items_
   
    render_table(padre,len(almacen.articulos),items_)

   
    # render_table(padre,len(almacen.articulos))
   
    

#Función para limpiar la lista de artículos en la interfaz
def limpiar_lista(tabla,cola):
             # 1. Remover el widget visual
        tabla.removeItemWidget(cola)

    # 2. Eliminar el item de la lista para que no quede ocupando espacio
        fila =  tabla.row(cola)
        tabla.takeItem(fila)


#Función para almacenar el índice del artículo a eliminar
def agrear_lista_elimar(row,c,padre):
    
    if c == 5:
        if padre.ventana_costo.isVisible():
            padre.ventana_costo.hide()

        if padre.ventana_actualizar_agotados.isVisible():
            padre.ventana_actualizar_agotados.hide()
        padre.ventana_actualizar_agotados.show()
        padre.ventana_actualizar_agotados.btn_actualizar_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        item_ = ""
        if almacen.item == "":
            item_ = almacen.articulos[row]
        else:
            item_ = almacen.item[row]
        
        padre.ventana_actualizar_agotados.nombre_articulo_2.setText(item_.nombre)
        # padre.ventana_actualizar_agotados.nombre_articulo_2.setReadOnly(True)

        padre.ventana_actualizar_agotados.cantidad_articulo_2.setText(str(item_.cantidad))
        padre.ventana_actualizar_agotados.precio_articulo_2.setText(str(item_.precio)) 
        padre.ventana_actualizar_agotados.costo.setText(str(item_.costo)) 
        
        
        if variable.mi_funcion_on :
            padre.ventana_actualizar_agotados.btn_actualizar_2.clicked.disconnect(variable.mi_funcion)
            variable.mi_funcion_on  = False 
        variable.mi_funcion = lambda:filtrar_valores(padre,item_)
        padre.ventana_actualizar_agotados.btn_actualizar_2.clicked.connect(variable.mi_funcion)
        variable.mi_funcion_on = True
        padre.ventana_actualizar_agotados.setWindowIcon(QIcon("./img/logo.png"))
        
    if c == 6:
       showVentanaCosto(padre,row)
        

    if  len(almacen.item) > 0 :
        for i,item in enumerate(almacen.item):
            if i == row:

                almacen.eliminadas =item
    else:
        almacen.eliminadas = row

#Función para renderizar la tabla de artículos en la interfaz   
@asyncSlot()
async def filtrar_valores(param1,item):
        
        nombre = param1.ventana_actualizar_agotados.nombre_articulo_2.text()
        cantidad = param1.ventana_actualizar_agotados.cantidad_articulo_2.text()
        precio = param1.ventana_actualizar_agotados.precio_articulo_2.text()
        costo = param1.ventana_actualizar_agotados.costo.text()
         
        if nombre == "" or cantidad == "" or precio == "":
            
            param1.tipo_msj.titulo = "Aviso"
            param1.tipo_msj.text = "Rellene los campos"
            param1.sendMsjWarning(param1.tipo_msj)
            return
        param2 = []
        param2.append(nombre)
        param2.append(precio)
        param2.append(cantidad)
        param2.append(costo)
        param2.append(item.id)
        param1.ventana_actualizar_agotados.close()
        await asyncio.sleep(0.5)
        await agregar(param1,param2)

def render_table(padre,cantida,item=False):
   
    
    Item_ = QListWidgetItem()
    tabla = QTableWidget(0,7)

    if padre.cola_item_almacen:
        limpiar_lista(padre.almacen.tabla_articulo,padre.cola_item_almacen)
    tabla.setHorizontalHeaderLabels(["ID","NOMBRE","CANTIDAD","PRECIO","COSTO","ACCION",""])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    # tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight( padre.almacen.tabla_articulo.height())
    tabla.cellClicked.connect(lambda row,c:agrear_lista_elimar(row,c,padre))
    tabla.horizontalHeaderItem(5).setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter )
    
    tabla.setColumnWidth(0,int((5/100)*tabla.width()))
    tabla.setColumnWidth(1,int((30/100)*tabla.width()))
    tabla.setColumnWidth(2,int((15/100)*tabla.width()))
    tabla.setColumnWidth(3,int((15/100)*tabla.width()))
    tabla.setColumnWidth(4,int((15/100)*tabla.width()))
    tabla.setColumnWidth(5,int((10/100)*tabla.width()))
    tabla.setColumnWidth(6,int((10/100)*tabla.width()))
    tabla.setStyleSheet('''
    QScrollBar:vertical{
                background: #1e1e1e;
                width: 12px;
                margin: 0px 0px 0px 0px;      
                        }
    QHeaderView::section {
        border: none;  /* Quita la línea separadora */
        padding: 4px;
        background-color: lightgray;
    }

''')
    tabla.verticalHeader().setVisible(False)
    
    #Si no hay un artículo específico, renderiza todos los artículos
    if not item:
        tabla.setRowCount(len(almacen.articulos))
        
        for i,articulo in enumerate(almacen.articulos):
            index=0
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.nombre)))
            tabla.setItem(i,index+2,QTableWidgetItem(formatearDigitos(str(articulo.cantidad))))
            tabla.setItem(i,index+3,QTableWidgetItem(formatearDigitos(str(articulo.precio)))) 
            tabla.setItem(i,index+4,QTableWidgetItem(formatearDigitos(str(articulo.costo)))) 
            tabla.setItem(i,index+5,QTableWidgetItem(str("Actualizar"))) 
            tabla.setItem(i,index+6,QTableWidgetItem(str("Ver"))) 
            accion = tabla.item(i,index+5)
            accion_2 = tabla.item(i,index+6)
            accion.setForeground(QColor("white")) 
            accion.setBackground(QColor("#232f42")) 
            accion.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            accion_2.setForeground(QColor("white")) 
            accion_2.setBackground(QColor("#232f42"))
            accion_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
          
    else:
       
        index=0
        tabla.setRowCount(len(item))
        
        for i,articulo in enumerate(item):
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.nombre)))
            tabla.setItem(i,index+2,QTableWidgetItem(formatearDigitos(str(articulo.cantidad))))
            tabla.setItem(i,index+3,QTableWidgetItem(formatearDigitos(str(articulo.precio)))) 
            tabla.setItem(i,index+4,QTableWidgetItem(formatearDigitos(str(articulo.costo)))) 
            tabla.setItem(i,index+5,QTableWidgetItem(str("Actualizar"))) 
            tabla.setItem(i,index+6,QTableWidgetItem(str("Ver"))) 
            accion = tabla.item(i,index+5)
            accion_2 = tabla.item(i,index+6)
            accion.setForeground(QColor("white")) 
            accion.setBackground(QColor("#232f42")) 
            accion.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            accion_2.setForeground(QColor("white")) 
            accion_2.setBackground(QColor("#232f42"))
            accion_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
       
 
    Item_.setSizeHint(tabla.sizeHint())
    padre.almacen.tabla_articulo.addItem(Item_)
    padre.almacen.tabla_articulo.setItemWidget(Item_,tabla)
    padre.cola_item_almacen = Item_
    
#Función para agregar un nuevo artículo al inventario    
async def agregar(padre,propiedades=False):
    from component.main_window import cargando
    await cargando(padre)
    await asyncio.sleep(0.5)
    id=""
    bandera = False
    if not propiedades:
        nombre = padre.almacen.nombre_articulo.text()
        precio = padre.almacen.precio_articulo.text()
        cantidad = padre.almacen.cantidad_articulo.text()
        costo = padre.almacen.costo.text()
    else:
        bandera = True
        nombre = propiedades[0]
        precio = str(propiedades[1])
        cantidad = str(propiedades[2])
        costo = str(propiedades[3])
        id= int(propiedades[4])
    cantidad = cantidad.strip()
    nombre = nombre.strip()

    #Verifica si los campos están vacíos
    if nombre == '' or precio.strip() == "" or cantidad ==""or costo == "":

        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = "Por favor rellena los campos"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    
    new_item = item(nombre,precio,cantidad,costo)
 
    for articulo in  almacen.articulos:
        if articulo.id == id:
            
            nueva_cant = int(cantidad) 
            
            new_item = item(nombre,precio,nueva_cant,costo,articulo.id)
            break

   
    if bandera == True:  
      
        await update_articulo(new_item,padre)
    else:

        #llamar a la db
        await insertar_articulo(new_item,padre)
        #almacen.articulos.append(new_item)

    render_table(padre,1)
    padre.main_window.cargando.hide()


#Función para eliminar un artículo del inventario
async def eliminar(padre):
    if almacen.eliminadas == "":
        padre.tipo_msj.text ="Selecciona un articulo para eliminar"
        padre.tipo_msj.titulo ="Aviso"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    item = ""
    is_int = False
    try:
        int(almacen.eliminadas)
        is_int= True
    except:
        is_int= False

    if is_int:
        item = almacen.articulos[almacen.eliminadas]
        almacen.eliminadas = item
    else:
        item = almacen.eliminadas

    padre.tipo_msj.titulo = "Aviso"
    padre.tipo_msj.text = (f"Seguro que quieres eliminar el artículo {item.nombre}?")

    if (padre.sendMsjWarning(padre.tipo_msj)) != 1024:
        return
    
    if almacen.eliminadas:
        id =""
        for i,item in enumerate(almacen.articulos):
                if item.id == almacen.eliminadas.id:
                        id = i
        await delete_articulo(almacen.articulos[id],padre)
        almacen.item =""
    else:
        await delete_articulo(almacen.articulos[almacen.eliminadas],padre)
    await buscar_articulo(padre)
    
    almacen.eliminadas=""

# Función para conectar acciones de los botones en la interfaz de almacenamiento
def conectar_botones_almacen(botones,padre):
   
    botones[0].clicked.connect(lambda:asyncio.create_task(agregar(padre)))
    botones[1].clicked.connect(lambda:asyncio.create_task(eliminar(padre)))   
    botones[2].clicked.connect(lambda:asyncio.create_task(actualizar_tabla(padre)))   
    botones[3].clicked.connect(lambda:mostrar_ventana_agotado(padre))
    botones[4].clicked.connect(lambda:showVentanaCosto(padre,0,True))
    padre.producto_agotado.buscador_agotado.textChanged.connect(lambda text:buscador_agotado(text,padre))
    padre.almacen.input_articulo.textChanged.connect(lambda text:buscar(text,padre))
    padre.producto_agotado.btn_actualizar.clicked.connect(lambda:renderVentanaAgotado(padre))
    
    for btn in botones:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
# Función para conectar acciones de los menús en la interfaz de almacenamiento


async def insertar_articulo(articulo,padre):
    from component.main_window import cargando
    await cargando(padre)
    await asyncio.sleep(0.5)
    
    try:
        # conn.commit()
        data = []
        data.append(articulo.nombre)
        data.append(articulo.cantidad)
        data.append(articulo.precio)
        data.append(articulo.costo)

        headers={
            "Content-Type":"Application/json",
            "id":"0"
        }

        resp = requests.post(os.getenv("URL")+"/api/almacen",data=json.dumps(data),headers=headers)
        data= resp.json()
        if not data["ok"]:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = data["res"]
            padre.sendMsjError(padre.tipo_msj)
            padre.main_window.cargando.hide()
            #aqui poner mens de error
            return
        #aqui pone rmsj de exito
        await buscar_articulo(padre)
        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = data["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        
      
    except:
        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
       
    
    # conn.close()
@asyncSlot()
async def buscar_articulo(padre,id=False):
    if id :
        from component.main_window import cargando
        await cargando(padre)
        await asyncio.sleep(0.5)
      
    almacen.articulos = []
    articulos =[]
    almacen.agotado = []
    URL = os.getenv("URL") + "/api/almacen"
   
    try:
        if api.session != "":
            if not api.session.closed:
                await api.session.close()
        api.session =  aiohttp.ClientSession()
        async with api.session.get(URL) as resp:
            data = await resp.json()
            if not data["ok"]:

                padre.tipo_msj.titulo = "Error"
                padre.tipo_msj.text = data["res"]
                padre.sendMsjError(padre.tipo_msj)
                
                return
           
            for fila in data["res"]:
                articulo=item(fila["nombre"],fila["precio"],fila["cantidad"],fila["costo"],fila["id"])
                articulos.append(articulo)
                if fila["cantidad"] == 0: 
                    almacen.agotado.append(articulo)
            almacen.articulos = articulos
            render_table(padre,1)
         
            await api.session.close()
            padre.caja.raise_()
            padre.main_window.cargando.hide()
            
    except Exception as e:
        print(e)
        await api.session.close()
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = f"Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
        padre.caja.raise_()
        

async def update_articulo(new_item,padre):
  
    from component.main_window import cargando
    await cargando(padre)
    await asyncio.sleep(0.5)
    data = []
    data.append(new_item.id)
    data.append(new_item.nombre)
    data.append(new_item.cantidad)
    data.append(int(new_item.precio))
    data.append(int(new_item.costo))
    

    try:
        if api.session != "":
            if not api.session.closed:
                await api.session.close()
        api.session =  aiohttp.ClientSession()
        headers={
            "Content-Type" : "Application/json",
            "id":"2"
        }
        URL = os.getenv("URL")+"/api/almacen"
        async with api.session.post(URL,data=json.dumps(data),headers=headers) as resp:
       
            info = await resp.json()
            if not info["ok"]:
            
                padre.tipo_msj.titulo = "Error"
                padre.tipo_msj.text = info["res"]
                padre.sendMsjError(padre.tipo_msj)
                return
            await buscar_articulo(padre)
            padre.main_window.cargando.hide()
            padre.tipo_msj.titulo = "Éxito"
            padre.tipo_msj.text = info["res"]
            padre.sendMsjSuccess(padre.tipo_msj)
            await api.session.close()
        
    except :
        #msj de conexcion fallida
        await api.session.close()
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
    

async def  delete_articulo(articulo, padre):
    from component.main_window import cargando
    await cargando(padre)
    await asyncio.sleep(0.5)
    try:
        headers={
            "Content-type": "Application/json" ,
            "id":"1"
                   }
        resp = requests.post(os.getenv("URL")+"/api/almacen",data=json.dumps({"_id":articulo.id}),headers=headers)
        data = resp.json()
        if not data["ok"]:
            #msj de error 
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = data["res"]
            padre.sendMsjError(padre.tipo_msj)
            
            return
        
            #msj de exitos
        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = data["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        
        
    except:
        #msj de conexxion fallida
     
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
        # conn.close()
        pass
    
async def render_almacen(padre):
    render_table(padre,len(almacen.articulos))
    
def mostrar_ventana_agotado(padre):

    if padre.producto_agotado.isVisible():
        padre.producto_agotado.hide()
    padre.producto_agotado.show()
    padre.producto_agotado.btn_actualizar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    renderVentanaAgotado(padre)

def renderVentanaAgotado(padre,item_=False):

    if len(almacen.agotado) ==0:
        padre.tipo_msj.titulo = "Aviso"
        padre.tipo_msj.text = "No hay productos agotados"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        
        return
    
    tabla = QTableWidget()
    tabla.setColumnCount(2)
    tabla.setHorizontalHeaderLabels(["ID","NOMBRE"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight(padre.producto_agotado.lista_agotado.height())
    if padre.ventana_agotado_cola:
        limpiar_lista(padre.producto_agotado.lista_agotado,padre.ventana_agotado_cola)
    item = QListWidgetItem()
    if item_ == False:
        tabla.setRowCount(len(almacen.agotado))
        index_column = 0
        for item_row,agotado in enumerate(almacen.agotado):
            tabla.setItem(item_row,index_column,QTableWidgetItem(str(agotado.id)))
            tabla.setItem(item_row,index_column+1,QTableWidgetItem(agotado.nombre))

    else:
        
        tabla.setRowCount(len(item_))
        index_column = 0
        for item_row,agotado in enumerate(item_):
            tabla.setItem(item_row,index_column,QTableWidgetItem(str(agotado.id)))
            tabla.setItem(item_row,index_column+1,QTableWidgetItem(agotado.nombre))
        

    item.setSizeHint(tabla.sizeHint())
    padre.producto_agotado.lista_agotado.addItem(item)
    padre.producto_agotado.lista_agotado.setItemWidget(item,tabla)
    padre.ventana_agotado_cola = item
    
def buscador_agotado(text,padre):

    encuentra = False
    agotados = []
    if text == "":
        renderVentanaAgotado(padre)
        return
    for agotado in almacen.agotado:
        
        if text.lower() in agotado.nombre.lower():
            agotados.append(agotado)
            encuentra = True
            

    if not encuentra:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "No se encuentra el artículo"
        padre.sendMsjError(padre.tipo_msj)
        return
    
    renderVentanaAgotado(padre,agotados)


def showVentanaCosto(padre,row,general=False):

    if padre.ventana_actualizar_agotados.isVisible():
        padre.ventana_actualizar_agotados.hide()

    if padre.ventana_costo.isVisible():
        padre.ventana_costo.hide()
        
    padre.ventana_costo.show()
    if general:
        costo_general = 0
        cantida_pacas = 0
        for item_ in almacen.articulos:
            cantida_pacas += item_.cantidad 
            costo_general += item_.cantidad * item_.costo
        padre.ventana_costo.titulo_costo.setText("Costo General")
        padre.ventana_costo.valor_costo.setText(formatearDigitos((costo_general)))
        padre.ventana_costo.valor_pacas.setText(formatearDigitos((cantida_pacas)))
        return
    item_ = ""
    if almacen.item == "":
        item_ = almacen.articulos[row]
    else:
        item_ = almacen.item[row]
    padre.ventana_costo.titulo_costo.setText("Costo " + str(item_.nombre))
    padre.ventana_costo.valor_costo.setText(formatearDigitos((item_.costo * item_.cantidad)))
    padre.ventana_costo.valor_pacas.setText(formatearDigitos((item_.cantidad)))
    
async def actualizar_tabla(padre):
    almacen.item = ""
    await buscar_articulo(padre,True)
