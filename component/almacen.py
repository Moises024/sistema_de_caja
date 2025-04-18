from PyQt6.QtWidgets import QTableWidgetItem,QListWidgetItem,QTableWidget,QSizePolicy,QHeaderView

#Clase para almacenar artículos en el inventario
class contenedorArticulo:
    articulos=[]
    item=""
    eliminadas=""
almacen =contenedorArticulo()

#Clase para representar un artículo
class item:
    
    def __init__(self,nombre,precio,cantidad):
        self.id = self.generador_id()
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def generador_id(self):
        id=0
        for t in almacen.articulos:
            id +=1
        return id 

#Función para verificar si un valor es un entero    
def isInt(valor):
    try:
        int(valor)
        return True
    except:
        return False

#Función para buscar un artículo en el inventario        
def buscar(padre):
    id = padre.almacen.input_articulo.text()
    item = ""
    bandera = False

    if isInt(id):
        id = int(id)
    
    #Busca el artículo en la lista de artículos
    for articulo in almacen.articulos:
        if  id == articulo.id or id == articulo.nombre:
            item = articulo
            bandera=True
    
    #Si no se encontró el artículo
    if not bandera:
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Artículo no encontrado"
        padre.sendMsjError(padre.tipo_msj)
        return
    render_table(padre,1,item)

#Función para limpiar la lista de artículos en la interfaz
def limpiar_lista(padre):
             # 1. Remover el widget visual
        padre.almacen.tabla_articulo.removeItemWidget(padre.cola_item)

    # 2. Eliminar el item de la lista para que no quede ocupando espacio
        fila =  padre.almacen.tabla_articulo.row(padre.cola_item)
        padre.almacen.tabla_articulo.takeItem(fila)

#Función para almacenar el índice del artículo a eliminar
def agrear_lista_elimar(row,c):
    almacen.eliminadas = row

#Función para renderizar la tabla de artículos en la interfaz   
def render_table(padre,cantida,item=""):
   
    Item_ = QListWidgetItem()
    tabla = QTableWidget(cantida,4)

    if padre.cola_item:
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
    padre.cola_item = Item_
    
#Función para agregar un nuevo artículo al inventario    
def agregar(padre):
    
    nombre = padre.almacen.nombre_articulo.text()
    precio = padre.almacen.precio_articulo.text()
    cantidad = padre.almacen.cantidad_articulo.text()
    
    #Verifica si los campos están vacíos
    if nombre.strip() == '' or precio.strip() == "" or cantidad.strip() =="":

        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = "Por favor rellena los campos"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    new_item = item(nombre,precio,cantidad)
    almacen.articulos.append(new_item)
    render_table(padre,1)

#Función para eliminar un artículo del inventario
def eliminar(padre):
    if almacen.eliminadas == "":
        padre.tipo_msj.text ="Selecciona articulo a eliminar"
        padre.tipo_msj.titulo ="Warning"
        padre.sendMsjWarningSingle(padre.tipo_msj)
        return
    del almacen.articulos[int(almacen.eliminadas)]
    render_table(padre,1)
    almacen.eliminadas=""

# Función para conectar acciones de los botones en la interfaz de almacenamiento
def conectar_botones_almacen(botones,padre):
    render_table(padre,len(almacen.articulos))
    botones[0].clicked.connect(lambda:buscar(padre))
    botones[1].clicked.connect(lambda:agregar(padre))
    botones[2].clicked.connect(lambda:eliminar(padre))   

# Función para conectar acciones de los menús en la interfaz de almacenamiento
def conectar_acciones_almacen(botones,padre):
    botones[1].triggered.connect(padre.salir)
    botones[0].triggered.connect(lambda:padre.change_window(padre.caja,3))
    pass

