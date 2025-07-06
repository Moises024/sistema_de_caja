from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView
from component.db import db
import sqlite3

#Clase para almacenar artículos en el inventario
class contenedorArticulo:
    articulos=[]
    item=""
    eliminadas=""
    agotado = []
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
def limpiar_lista(tabla,cola):
             # 1. Remover el widget visual
        tabla.removeItemWidget(cola)

    # 2. Eliminar el item de la lista para que no quede ocupando espacio
        fila =  tabla.row(cola)
        tabla.takeItem(fila)


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
        limpiar_lista(padre.almacen.tabla_articulo,padre.cola_item_almacen)
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
        if articulo.nombre.lower() == nombre.lower():
            bandera = True
            nueva_cant = int(cantidad) + int(articulo.cantidad)
            new_item = item(articulo.nombre,precio,nueva_cant)
            break

        
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
    botones[3].clicked.connect(lambda:mostrar_ventana_agotado(padre))
    padre.producto_agotado.buscador_agotado.textChanged.connect(lambda text:buscador_agotado(text,padre))
    padre.almacen.input_articulo.textChanged.connect(lambda text:buscar(text,padre))
# Función para conectar acciones de los menús en la interfaz de almacenamiento


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
    almacen.agotado = []
    for fila in cursor.fetchall():
        articulo=item(fila[1],fila[3],fila[2],fila[0])
        articulos.append(articulo)
        if fila[2] == 0:
            almacen.agotado.append(articulo)

            
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
def mostrar_ventana_agotado(padre):

    if padre.producto_agotado.isVisible():
        padre.producto_agotado.hide()
    padre.producto_agotado.show()

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
       
        tabla.setRowCount(1)
        tabla.setItem(0,0,QTableWidgetItem(str(item_.id)))
        tabla.setItem(0,1,QTableWidgetItem(item_.nombre))

    item.setSizeHint(tabla.sizeHint())
    padre.producto_agotado.lista_agotado.addItem(item)
    padre.producto_agotado.lista_agotado.setItemWidget(item,tabla)
    padre.ventana_agotado_cola = item
    
def buscador_agotado(text,padre):

    encuentra = False

    if text == "":
        renderVentanaAgotado(padre)
        return
    for agotado in almacen.agotado:
        
        if text.lower() in agotado.nombre.lower():
            renderVentanaAgotado(padre,agotado)

            encuentra = True
            break

    if not encuentra:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "No se encuentra el artículo"
        padre.sendMsjError(padre.tipo_msj)



        
