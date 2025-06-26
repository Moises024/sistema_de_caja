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
    input_usuario = login.input_nombre_usuario
    input_contra = login.input_login
    if input_usuario.text() == "":
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Por favor rellena el campo de usuario"
        padre.sendMsjError(padre.tipo_msj)
        input_usuario.setFocus()
        return
    if input_contra.text() == "":
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Por favor rellena el campo de contraseña"
        padre.sendMsjError(padre.tipo_msj)
        input_contra.setFocus()
        return
    contra_ = padre.password
    usuario_ = input_usuario.text()
    dataDataBase = db()
    conn = dataDataBase.crearConnexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE  usuario=?",(usuario_,))
        usuario = cursor.fetchone()
        
        if not usuario:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Usuario incorrecto"
            padre.sendMsjError(padre.tipo_msj)
            input_usuario.setFocus()
            return
    

        cursor.execute("SELECT * FROM usuarios WHERE contra=? and usuario=?",(contra_,usuario_))
        usuario = cursor.fetchone()

        if usuario:
            user.nombre = usuario[1]
            user.apellido = usuario[3] 
            user.id = usuario[0]
            user.rol =usuario[4]
            padre.usuario = user
            input_contra.setText('')
            input_usuario.setText('')
            padre.tiempo_inicio = datetime.datetime.now()
            padre.change_window(caja,1)
        else:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Contraseña incorrecta"
            padre.sendMsjError(padre.tipo_msj)
            input_contra.setFocus()

    except sqlite3.Error as err:
        print("error",err)
        
    conn.close()

def conectar_botones_login(botones,login,padre,caja):
    
    #Acción de los botones
    
    botones[0].clicked.connect(lambda:datos_usurios(login,padre,caja))
    


def conectar_acciones_login(login,padre):
    login.salir.triggered.connect(padre.salir)
    

