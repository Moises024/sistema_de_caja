from component.db import db
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
import sqlite3
import os
import requests
import json
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def registrar_usuario(registrar,padre,cargando):
    await cargando(padre)
    await asyncio.sleep(2)
    nombre = registrar.input_nombre
    apellido = registrar.input_apellido
    contra = registrar.input_contra
    usuario = registrar.input_usuario
    array_input = [nombre,apellido,usuario,contra]
    
    for index,input in enumerate(array_input):
        if input.text() =='':
            padre.tipo_msj.titulo = "Aviso"
            padre.tipo_msj.text = "Rellene el campo"
            padre.sendMsjWarningSingle(padre.tipo_msj)
            input.setFocus()
            padre.main_window.cargando.hide()
            return
        else:
             array_input[index] = input.text()

    #llamar data base
    # baseDeDatos = db()
    # conn = baseDeDatos.crearConnexion()
    # cursor = conn.cursor()
    is_name = False
    is_usuario = False
    
    try:
        # cursor.execute("SELECT * FROM usuarios WHERE lower(nombre)=lower(?) and lower(apellido)=lower(?)",(array_input[0],array_input[1]))
        # nombre = cursor.fetchone()
        resp = requests.get(os.getenv("URL")+"/api/user")
        data_json  = resp.json()
        data = data_json["res"]

        for user in data:
            if user["nombre"].lower() == nombre.lower():
                is_name = True
                break
            if user["usuario"].lower() == usuario.lower():
                is_usuario = True
                break
            
        # cursor.execute("SELECT * FROM usuarios WHERE usuario = ?",(array_input[2],))
        # usuario = cursor.fetchone()
        
       
        if is_name:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Nombre/apellido existente"
            padre.sendMsjError(padre.tipo_msj)
            return
        
        if is_usuario:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Usuario ya existente"
            padre.sendMsjError(padre.tipo_msj)
            return
    
        nombre = array_input[0]
        apellido =array_input[1]
        usuario =array_input[3]
        contra = array_input[2]

        # cursor.execute("INSERT INTO usuarios(nombre,apellido,usuario,contra) VALUES(?, ?, ?, ?)",(nombre,apellido,usuario,contra))
        # conn.commit()
        data = []
        data.append(nombre)
        data.append(contra)
        data.append(apellido)
        data.append(usuario)
        headers = {
            "Content-Type":"Application/json"
        }
        resp = requests.post(os.getenv("URL")+"/api/user",data=json.dumps(data),headers=headers)
        res = resp.json()
        
        if not res["ok"]:
            print(res['res'])
            return
        padre.main_window.cargando.hide()
        padre.tipo_msj.titulo = "Éxito"
        padre.tipo_msj.text = res["res"]
        padre.sendMsjSuccess(padre.tipo_msj)
        registrar.input_nombre.setText("") 
        registrar.input_apellido.setText("")
        registrar.input_contra.setText("")
        registrar.input_usuario.setText("")

    except sqlite3.Error as err:
       
        if err.sqlite_errorcode == 2067 :
            if err.args[0] == 'UNIQUE constraint failed: usuarios.contra':
                padre.tipo_msj.text = "Ingrese otra contraseña"
                
        else:
            padre.tipo_msj.text = "No se pudo crear el usuario"
        # conn.close()
        padre.tipo_msj.titulo = "Error"
        padre.sendMsjError(padre.tipo_msj)
        padre.main_window.cargando.hide()
        return
    # conn.close()


def conectar_botones_registrar(botones,registrar,padre):
    from component.main_window import cargando
    botones[0].clicked.connect(lambda:asyncio.create_task(registrar_usuario(registrar,padre,cargando)))
    for btn in botones:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
