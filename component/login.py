
import datetime
import sqlite3
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt      
import os
import requests
import json
from dotenv import load_dotenv                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
class usuario:
    id=""
    nombre=""
    apellido =""
    rol=""
user_ = usuario()

def datos_usuarios(login,padre,main_window):
    usuario = False
    contra = False
    user_data = False
    input_usuario = login.input_nombre_usuario
    input_contra = login.input_login
    if input_usuario.text() == "":
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Por favor rellena el campo de usuario"
        padre.sendMsjError(padre.tipo_msj)
        input_usuario.setFocus()
        padre.release_enter =  True
        return
    if input_contra.text() == "":
        padre.tipo_msj.titulo = "Error"
        padre.tipo_msj.text = "Por favor rellena el campo de contraseña"
        padre.sendMsjError(padre.tipo_msj)
        input_contra.setFocus()
        padre.release_enter =  True
        return
    contra_ = padre.password
    usuario_ = input_usuario.text()
    # dataDataBase = db()
    # conn = dataDataBase.crearConnexion()
    # cursor = conn.cursor()
    try:
        # cursor.execute("SELECT * FROM usuarios WHERE  usuario=?",(usuario_,))
        # usuario = cursor.fetchone()
        resp = requests.get(os.getenv("URL")+"/api/user")
        data_json  = resp.json()
        data = data_json["res"]
       
        for user in data:
            
            if user["usuario"] == usuario_.strip():
                contra = True
                
            if user["contra"] == contra_.strip():
                usuario = True
                user_data = user
                break
        
        if not contra:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Usuario incorrecto"
            padre.sendMsjError(padre.tipo_msj)
            input_usuario.setFocus()
            padre.release_enter =  True

            return
    

        # cursor.execute("SELECT * FROM usuarios WHERE contra=? and usuario=?",(contra_,usuario_))
        # usuario = cursor.fetchone()
       
        if user_data:
            user_.nombre = user_data["nombre"]
            user_.apellido = user_data["apellido"] 
            user_.id = user_data["id"] 
            user_._id = user_data["_id"] 
            user_.rol =user_data["rol"]
            padre.usuario = user_
            input_contra.setText('')
            input_usuario.setText('')
            padre.tiempo_inicio = datetime.datetime.now()
            padre.change_window(main_window,padre.MAIN_WINDOW)
        else:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Contraseña incorrecta"
            padre.sendMsjError(padre.tipo_msj)
            input_contra.setFocus()
            padre.release_enter =  True
            padre.password =""

    except sqlite3.Error as err:
        print("error",err)
        
        
    # conn.close()

def conectar_botones_login(botones,login,padre,caja):
    
    #Acción de los botones
    
    botones[0].clicked.connect(lambda:datos_usuarios(login,padre,padre.main_window))
    login.btn_acceder.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

def conectar_acciones_login(login,padre):
    login.salir.triggered.connect(padre.salir)
    

