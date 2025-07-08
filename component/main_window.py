from PyQt6.QtWidgets import QLabel,QWidget
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QCursor,QPixmap


class labels:
    names=[]
    clicked_bottons=[]
array_label = labels()
array_label.names=["Facturar","Inventario","Almacen","Registrar"]
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
            print("entre")
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
         label["link"].clicked.connect(lambda:activeLink(padre,label))

def activeLink(padre,label):
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
        padre.change_window(padre.caja,padre.CAJA_CODE)
    if label["id"]== 1 and padre.usuario.rol  == 3:
        padre.change_window(padre.inventario,padre.INVENTARIO_CODE)
    if label["id"]== 2 and padre.usuario.rol  == 3:
        padre.change_window(padre.almacen,padre.ALMACEN_CODE)
    if label["id"] ==3 and padre.usuario.rol  == 3:
        padre.change_window(padre.registrar,padre.REGISTRAR_CODE)

def agregar_salir(main_window,padre):
    
    pixmap = QPixmap("./img/apagar.png")
    
    
    salir = Create_link("Salir")
    salir.setFixedSize(60,45)
    redimencionada = pixmap.scaled(salir.width(), salir.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    salir.setPixmap(redimencionada)
    parent = main_window.header.findChild(QWidget,"container_user",)
    header_width = main_window.header.width()
    user_width = (40/110) * header_width
    parent.setFixedWidth(int(user_width))
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
    
    salir.move(parent.width()-60,int(int(parent.height()/2)-20))
    salir.clicked.connect(padre.salir)
    

