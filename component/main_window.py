from PyQt6.QtWidgets import QLabel,QWidget
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QCursor,QPixmap
import asyncio
from component.almacen import buscar_articulo
from component.inventario import buscar_facturas
from component.caja import buscar_articulos

async def cargando(padre):
    padre.main_window.cargando.show()
    padre.main_window.cargando.move(0,0)
    padre.main_window.cargando.setAlignment(Qt.AlignmentFlag.AlignCenter)
    padre.main_window.cargando.setFixedSize(padre.main_window.width(),padre.main_window.height())
    padre.main_window.cargando.setText("Cargando...")
    padre.main_window.cargando.setStyleSheet('''
    QLabel{
                
                font-size:30px;      
                color:#fff;
                background-color:rgba(0, 0, 0, 150);                                 }
''')
    padre.main_window.cargando.raise_()

class labels:
    names=[]
    clicked_bottons=[]
array_label = labels()
array_label.names=["Facturar","Inventario","Almacén","Registrar"]

class Create_link(QLabel):
    clicked = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
    def mousePressEvent(self,event):
        self.clicked.emit()
        super().mousePressEvent(event)

       
def connectar_botones_main(botones,padre):
    if len(array_label.clicked_bottons) > 0:
        for i,label in enumerate(array_label.clicked_bottons):
            label["link"].deleteLater()
    array_label.clicked_bottons = []
   
    for i,label in enumerate(botones):
        text = array_label.names[i]
        label.setText('')
       
        if padre.usuario.rol == 3 or i ==0:
            label_click = Create_link(label)
            label_click.setText(text)
            label_click.setFixedSize(label.width(),label.height())
            array_label.clicked_bottons.append({"link":label_click,"id":i})
    
    for label in array_label.clicked_bottons:
        label["link"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label["link"].setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        label["link"].setOpenExternalLinks(False)
        label["link"].setStyleSheet('''
            QLabel{
                    border-radius:10px;
                    text-align:center;
                    padding:10px;
                    height:100%;
                    color:#f1f1f1;
            }
            QLabel::hover{ 
                            background-color:#232f42;

                            }
        
        ''')
        connet_click(label,padre)
    
def connet_click(label,padre):
         label["link"].clicked.connect(lambda:asyncio.create_task(activeLink(padre,label)))

async def activeLink(padre,label):
    for link in array_label.clicked_bottons:
        if label["id"] == link["id"]:
            link["link"].setStyleSheet('''
            QLabel{
                    border-radius:10px;
                    text-align:center;
                    padding:10px;
                    background-color: rgba(167, 167, 167, 100);
                    height:100%;
            }
            QLabel::hover{
                            background-color:#232f42;

                            }
        
        ''')
        else:
            link["link"].setStyleSheet('''
            QLabel{
                    border-radius:10px;
                    text-align:center;
                    padding:10px;
                    background-color:transparent;
                    height:100%;
            }
            QLabel::hover{
                            background-color:#232f42;

                            }
        
        ''')
        
       
    if label["id"] == 0:
        await cargando(padre)
        
        padre.change_window(padre.caja,padre.CAJA_CODE)
        padre.caja.lower()
        await buscar_articulos(padre)
   
    if label["id"]== 1 and padre.usuario.rol  == 3:
        await cargando(padre)
        padre.change_window(padre.inventario,padre.INVENTARIO_CODE)
        await buscar_facturas(padre)

    if label["id"]== 2 and padre.usuario.rol  == 3:
        await cargando(padre)
        padre.change_window(padre.almacen,padre.ALMACEN_CODE)
        await buscar_articulo(padre)
        # buscar_articulo(padre)
        # render_almacen(padre)
   
    if label["id"] ==3 and padre.usuario.rol  == 3:
        await cargando(padre)
        padre.change_window(padre.registrar,padre.REGISTRAR_CODE)
        padre.main_window.cargando.hide()

def agregar_salir(main_window,padre):
    
    pixmap = QPixmap("./img/apagar.png")
    
    salir = Create_link("Salir")
    contenedor_user = main_window.header.findChild(QWidget,"container_user",)
    parent = contenedor_user.findChild(QWidget,"contenedor_btn_salir",) 
    contenedor_user.setFixedWidth(429)
   
    width_user = contenedor_user.width()
    padre.btn_salir = salir
    salir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    salir.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    salir.setOpenExternalLinks(False)
    salir.setParent(parent)
    salir.setStyleSheet('''
                    
        QLabel{
                        
                        color: rgb(255, 255, 255);
	                        font: 100 18pt "Dubai";
                        padding-left:10px;
                        border-radius:50px;
                        }

''')
    
    salir.setFixedSize(parent.width(),parent.height())
    redimencionada = pixmap.scaled(parent.width(), parent.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    salir.setPixmap(redimencionada)
    parent.move(width_user-parent.width(),int(int(parent.height()/2)-6))
    salir.clicked.connect(padre.salir)
    
