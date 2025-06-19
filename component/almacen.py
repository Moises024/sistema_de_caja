from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView
from component.db import db
import sqlite3

#Clase para almacenar artículos en el inventario
class contenedorArticulo:
    articulos=[]
    item=""
    eliminadas=""
almacen = contenedorArticulo()

#Clase para representar un artículo
class item:
    
    def __init__(self,nombre,precio,cantidad,id=""):
        self.id =id 
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def generador_id(self):
        
        guardar = ""

        if len(almacen.articulos) == 0:
            return 1

        for i_j,t in enumerate(almacen.articulos):
            valor = t
            if guardar == "":
                guardar = int(valor.id)

            for i_i,z in enumerate(almacen.articulos):
                if guardar < int(z.id):
                    guardar = z.id

        guardar += 1
        return guardar 


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
    item = ""
    bandera = False

    if isInt(text): 
        id = int(text)
    
    #Busca el artículo en la lista de artículos
    for articulo in almacen.articulos:
    
        if  id == False:
            if nombre.lower() in articulo.nombre.lower():
             item = articulo
             bandera=True
        else:
            if id == int(articulo.id):
                item = articulo
                bandera=True

    #Si no se encontró el artículo
    if not bandera:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Artículo no encontrado"
        padre.sendMsjError(padre.tipo_msj)
        return
    almacen.item = item
    render_table(padre,1,item)

#Función para limpiar la lista de artículos en la interfaz
def limpiar_lista(padre):
             # 1. Remover el widget visual
        padre.almacen.tabla_articulo.removeItemWidget(padre.cola_item_almacen)

    # 2. Eliminar el item de la lista para que no quede ocupando espacio
        fila =  padre.almacen.tabla_articulo.row(padre.cola_item_almacen)
        padre.almacen.tabla_articulo.takeItem(fila)

#Función para almacenar el índice del artículo a eliminar
def agrear_lista_elimar(row,c):
    if  almacen.item:
        almacen.eliminadas =almacen.item
    else:
        almacen.eliminadas = row

#Función para renderizar la tabla de artículos en la interfaz   
def render_table(padre,cantida,item=""):
    buscar_articulo()
    Item_ = QListWidgetItem()
    tabla = QTableWidget(cantida,4)

    if padre.cola_item_almacen:
        limpiar_lista(padre)
    tabla.setHorizontalHeaderLabels(["ID","NOMBRE","CANTIDAD","PRECIO"])
    tabla.resizeColumnsToContents()
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setFixedHeight( padre.almacen.tabla_articulo.height())
    tabla.cellClicked.connect(agrear_lista_elimar)

    #Si no hay un artículo específico, renderiza todos los artículos
    if item == "":
        tabla.setRowCount(len(almacen.articulos))
        for i,articulo in enumerate(almacen.articulos):
            index=0
            tabla.setItem(i,index,QTableWidgetItem(str(articulo.id)))
            tabla.setItem(i,index+1,QTableWidgetItem(str(articulo.nombre)))
            tabla.setItem(i,index+2,QTableWidgetItem(str(articulo.cantidad)))
            tabla.setItem(i,index+3,QTableWidgetItem(str(articulo.precio))) 
    else:
        index=0
        tabla.setItem(index,index   ,QTableWidgetItem(str(item.id)))
        tabla.setItem(index,index+1 ,QTableWidgetItem(str(item.nombre)))
        tabla.setItem(index,index+2 ,QTableWidgetItem(str(item.cantidad)))
        tabla.setItem(index,index+3 ,QTableWidgetItem(str(item.precio)))
 

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
        if articulo.nombre == nombre:
            bandera = True
            nueva_cant = int(cantidad) + int(articulo.cantidad)
            new_item = item(nombre,precio,nueva_cant)

        
    if bandera == True:
        update_articulo(new_item)
    else:
        #llamar a la db
        insertar_articulo(new_item)
        #almacen.articulos.append(new_item)

        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = "Artículo agregado correctamente"
        padre.sendMsjSuccess(padre.tipo_msj)

    render_table(padre,1)


#Función para eliminar un artículo del inventario
def eliminar(padre):
    if almacen.eliminadas == "":
        padre.tipo_msj.text ="Selecciona un articulo para eliminar"
        padre.tipo_msj.titulo ="Warning"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    item = ""
    if almacen.item:
        item = almacen.item
    else:
        item = almacen.articulos[almacen.eliminadas]

    padre.tipo_msj.titulo = "Warning"
    padre.tipo_msj.text = (f"Seguro que quieres eliminar el artículo {item.nombre}?")

    if (padre.sendMsjWarning(padre.tipo_msj)) != 1024:
        return
    
    if almacen.item:
        id =""
        for i,item in enumerate(almacen.articulos):
                if item.id == almacen.item.id:
                        id = i
        delete_articulo(almacen.articulos[id])
        almacen.item =""
    else:
        delete_articulo(almacen.articulos[almacen.eliminadas])
        

    render_table(padre,1)
    almacen.eliminadas=""

# Función para conectar acciones de los botones en la interfaz de almacenamiento
def conectar_botones_almacen(botones,padre):
   
    botones[0].clicked.connect(lambda:agregar(padre))
    botones[1].clicked.connect(lambda:eliminar(padre))   
    botones[2].clicked.connect(lambda:render_table(padre,len(almacen.articulos)))   

# Función para conectar acciones de los menús en la interfaz de almacenamiento
def conectar_acciones_almacen(botones,padre):
    botones[1].triggered.connect(padre.salir)
    botones[0].triggered.connect(lambda:padre.change_window(padre.caja,3))
    padre.almacen.input_articulo.textChanged.connect(lambda text:buscar(text,padre))
    
    pass

def insertar_articulo(articulo):
    database = db()
    conn = database.crearConnexion() 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articulos(nombre,cantidad,precio) values(?,?,?)",(articulo.nombre,articulo.cantidad,articulo.precio))
    try:
        conn.commit()
    except sqlite3.Error as err:
        print(err)
    conn.close()

def buscar_articulo():
    database = db()
    conn = database.crearConnexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articulos")
    articulos =[]
    for fila in cursor.fetchall():
        articulo=item(fila[1],fila[3],fila[2],fila[0])
        articulos.append(articulo)
    almacen.articulos = articulos
    conn.close() 

def update_articulo(new_item):
    database = db()
    conn = database.crearConnexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE articulos SET nombre=?, cantidad=?, precio=? where nombre=?",(new_item.nombre,new_item.cantidad,new_item.precio,new_item.nombre))
    try:
        conn.commit()
    except sqlite3.Error as err:
        print(err)
    conn.close()

def  delete_articulo(articulo):
    database = db()
    conn = database.crearConnexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articulos WHERE nombre=?",(articulo.nombre,))
    try:
        conn.commit()
    except sqlite3.Error as err:
        print(err)
    conn.close()
    
def render_almacen(padre):
    render_table(padre,len(almacen.articulos))
