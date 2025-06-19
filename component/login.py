from component.db import db
import datetime
import sqlite3

class usuario:
    id=""
    nombre=""
    apellido =""
    rol=""
user = usuario()

def datos_usurios(login,padre,caja):
   
    contra = padre.password
    dataDataBase = db()
    conn = dataDataBase.crearConnexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE contra=?",(contra,))
        usuario = cursor.fetchone()
      
        if usuario:
            user.nombre = usuario[1]
            user.apellido = usuario[3]
            user.id = usuario[0]
            user.rol =usuario[4]
            padre.usuario = user
            login.input_login.setText('')
            padre.tiempo_inicio = datetime.datetime.now()
            padre.change_window(caja,1)
        else:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Código inválido"
            padre.sendMsjError(padre.tipo_msj)
            return
    except sqlite3.Error as err:
        print(err)
        
    conn.close()

def conectar_botones_login(botones,login,padre,caja):
    
    #Acción de los botones
    botones[0].clicked.connect(lambda:padre.teclado(0,login)) 
    botones[1].clicked.connect(lambda:padre.teclado(1,login)) 
    botones[2].clicked.connect(lambda:padre.teclado(2,login)) 
    botones[3].clicked.connect(lambda:padre.teclado(3,login)) 
    botones[4].clicked.connect(lambda:padre.teclado(4,login)) 
    botones[5].clicked.connect(lambda:padre.teclado(5,login)) 
    botones[6].clicked.connect(lambda:padre.teclado(6,login)) 
    botones[7].clicked.connect(lambda:padre.teclado(7,login)) 
    botones[8].clicked.connect(lambda:padre.teclado(8,login))  
    botones[9].clicked.connect(lambda:padre.teclado(9,login)) 
    botones[10].clicked.connect(lambda:datos_usurios(login,padre,caja))
    botones[11].clicked.connect(lambda:padre.borrar(login))


def conectar_acciones_login(login,padre):
    login.salir.triggered.connect(padre.salir)
    login.registrar.triggered.connect(lambda:padre.change_window(padre.registrar,5))

