from PyQt6.QtWidgets import QLabel,QWidget
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QCursor


class labels:
    clicked_bottons=[]
array_label = labels()
class Create_link(QLabel):
    clicked = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
    def mousePressEvent(self,event):
        self.clicked.emit()
        super().mousePressEvent(event)

def connectar_botones_main(botones,padre):
    agregar_salir(padre.main_window,padre)
    for i,label in enumerate(botones):
        text = label.text()
        label.setText('')
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
                    background-color:#232f42;
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
            }
            QLabel::hover{
                            background-color:#232f42;

                            }
        
        ''')
    if label["id"] == 0:
        padre.change_window(padre.caja,padre.CAJA_CODE)
    if label["id"]== 1:
        padre.change_window(padre.inventario,padre.INVENTARIO_CODE)

def agregar_salir(main_window,padre):
    salir = Create_link("Salir")
    parent = main_window.header.findChild(QWidget,"container_user",)
    header_width = main_window.header.width()
    user_width = (40/100) * header_width
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
                        }
        QLabel::hover{
                            background-color:#232f42;
                            

                            }
''')
    salir.setFixedSize(80,30)
    salir.move(parent.width()-80,int(int(parent.height()/2)-20))
    salir.clicked.connect(padre.salir)
    

