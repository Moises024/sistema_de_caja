from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
import threading
import requests
import aiohttp
import os
from dotenv import load_dotenv
import json
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
#Clase para representar un artículo
class item:
    
    def __init__(self,nombre,precio,cantidad,id=""):
        self.id =id 
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad




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
def agrear_lista_elimar(row,c):
    if  len(almacen.item) > 0 :
        for i,item in enumerate(almacen.item):
            if i == row:

                almacen.eliminadas =item
    else:
        almacen.eliminadas = row

#Función para renderizar la tabla de artículos en la interfaz   


def render_table(padre,cantida,item=False):
    
    
    Item_ = QListWidgetItem()
    tabla = QTableWidget(0,4)

    if padre.cola_item_almacen:
        limpiar_lista(padre.almacen.tabla_articulo,padre.cola_item_almacen)
    tabla.setHorizontalHeaderLabels(["ID","NOMBRE","CANTIDAD","PRECIO"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight( padre.almacen.tabla_articulo.height())
    tabla.cellClicked.connect(agrear_lista_elimar)
   
    #Si no hay un artículo específico, renderiza todos los artículos
    if not item:
        tabla.setRowCount(len(almacen.articulos))
        
        for i,articulo in enumerate(almacen.articulos):
            index=0
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.nombre)))
            tabla.setItem(i,index+2,QTableWidgetItem(str(articulo.cantidad)))
            tabla.setItem(i,index+3,QTableWidgetItem(str(articulo.precio))) 

    else:
       
        index=0
        tabla.setRowCount(len(item))
        
        for i,articulo in enumerate(item):
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.nombre)))
            tabla.setItem(i,index+2,QTableWidgetItem(str(articulo.cantidad)))
            tabla.setItem(i,index+3,QTableWidgetItem(str(articulo.precio))) 
       
 

    Item_.setSizeHint(tabla.sizeHint())
    padre.almacen.tabla_articulo.addItem(Item_)
    padre.almacen.tabla_articulo.setItemWidget(Item_,tabla)
    padre.cola_item_almacen = Item_
    
#Función para agregar un nuevo artículo al inventario    
def agregar(padre):
    
    nombre = padre.almacen.nombre_articulo.text()
    precio = padre.almacen.precio_articulo.text()
    cantidad = padre.almacen.cantidad_articulo.text()
    
    cantidad = cantidad.strip()
    nombre = nombre.strip()
    bandera = False

    #Verifica si los campos están vacíos
    if nombre == '' or precio.strip() == "" or cantidad =="":

        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = "Por favor rellena los campos"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    new_item = item(nombre,precio,cantidad)
    
    for articulo in  almacen.articulos:
        if articulo.nombre.lower() == nombre.lower():
            bandera = True
            nueva_cant = int(cantidad) + int(articulo.cantidad)
            new_item = item(articulo.nombre,precio,nueva_cant)
            break

        
    if bandera == True:
       
        update_articulo(new_item,padre)
    else:
        
        #llamar a la db
        insertar_articulo(new_item,padre)
        #almacen.articulos.append(new_item)

    render_table(padre,1)


#Función para eliminar un artículo del inventario
def eliminar(padre):
    if almacen.eliminadas == "":
        padre.tipo_msj.text ="Selecciona un articulo para eliminar"
        padre.tipo_msj.titulo ="Warning"
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

    print(item)
    padre.tipo_msj.titulo = "Warning"
    padre.tipo_msj.text = (f"Seguro que quieres eliminar el artículo {item.nombre}?")

    if (padre.sendMsjWarning(padre.tipo_msj)) != 1024:
        return
    
    if almacen.eliminadas:
        id =""
        for i,item in enumerate(almacen.articulos):
                if item.id == almacen.eliminadas.id:
                        id = i
        delete_articulo(almacen.articulos[id],padre)
        almacen.item =""
    else:
        delete_articulo(almacen.articulos[almacen.eliminadas],padre)
    buscar_articulo(padre)
    render_table(padre,1)
    almacen.eliminadas=""

# Función para conectar acciones de los botones en la interfaz de almacenamiento
def conectar_botones_almacen(botones,padre):
   
    botones[0].clicked.connect(lambda:agregar(padre))
    botones[1].clicked.connect(lambda:eliminar(padre))   
    botones[2].clicked.connect(lambda:render_table(padre,len(almacen.articulos)))   
    botones[3].clicked.connect(lambda:mostrar_ventana_agotado(padre))
    padre.producto_agotado.buscador_agotado.textChanged.connect(lambda text:buscador_agotado(text,padre))
    padre.almacen.input_articulo.textChanged.connect(lambda text:buscar(text,padre))
    for btn in botones:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
# Función para conectar acciones de los menús en la interfaz de almacenamiento


async def insertar_articulo(articulo,padre):
    # database = db()
    # conn = database.crearConnexion() 
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO articulos(nombre,cantidad,precio) values(?,?,?)",(articulo.nombre,articulo.cantidad,articulo.precio))
    
    try:
        # conn.commit()
        data = []
        data.append(articulo.nombre)
        data.append(articulo.cantidad)
        data.append(articulo.precio)
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
            
            #aqui poner mens de error
            return
        #aqui pone rmsj de exito
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = data["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        await buscar_articulo(padre)
      
    except:
   
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
    
    # conn.close()

async def buscar_articulo(padre):
  
    # database = db()
    # conn = database.crearConnexion()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM articulos")
   
    # for fila in cursor.fetchall():
    #     articulo=item(fila[1],fila[3],fila[2],fila[0])
    #     articulos.append(articulo)
    #     if fila[2] == 0:
    #         almacen.agotado.append(articulo)

            
    almacen.articulos = []

    # conn.close() 
    articulos =[]
    almacen.agotado = []
    URL = os.getenv("URL") + "/api/almacen"
   
    try:
        if api.session != "":
            if not api.session.closed:
                await api.session.close()
        api.session =  aiohttp.ClientSession()
        async with api.session.get(URL) as resp:
            print("funcionando")
            data = await resp.json()
            if not data["ok"]:

                padre.tipo_msj.titulo = "Error"
                padre.tipo_msj.text = data["res"]
                padre.sendMsjError(padre.tipo_msj)
                
                return
            for fila in data["res"]:
                articulo=item(fila["nombre"],fila["precio"],fila["cantidad"],fila["id"])
                articulos.append(articulo)
                if fila["cantidad"] == 0: 
                    almacen.agotado.append(articulo)
            almacen.articulos = articulos
            render_table(padre,1)
            await api.session.close()
            padre.main_window.cargando.hide()
            padre.caja.raise_()
            
    except Exception as e:
        print(e)
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = f"Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
        padre.caja.raise_()
        
    
   
    


def update_articulo(new_item,padre):
    # database = db()
    # conn = database.crearConnexion()
    # cursor = conn.cursor()
    # cursor.execute("UPDATE articulos SET nombre=?, cantidad=?, precio=? where nombre=?",(new_item.nombre,new_item.cantidad,new_item.precio,new_item.nombre))
    # try:
    #     conn.commit()
    # except sqlite3.Error as err:
    #     print(err)
    # conn.close()
    data = []
    data.append(new_item.nombre)
    data.append(new_item.cantidad)
    data.append(int(new_item.precio))
    data.append(new_item.nombre)
    

    try:
        headers={
            "Content-Type" : "Application/json",
            "id":"2"
        }
        resp = requests.post(os.getenv("URL")+"/api/almacen",data=json.dumps(data),headers=headers)
        info = resp.json()
        if not info["ok"]:
        
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = info["res"]
            padre.sendMsjError(padre.tipo_msj)
            return
         
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = info["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        buscar_articulo(padre)
    except :
        #msj de conexcion fallida
    
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
    

def  delete_articulo(articulo, padre):
    # database = db()
    # conn = database.crearConnexion()
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM articulos WHERE nombre=?",(articulo.nombre,))
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
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = data["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        
        

    except:
        #msj de conexxion fallida
     
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Conexión fallida"
        padre.sendMsjError(padre.tipo_msj)
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



        
