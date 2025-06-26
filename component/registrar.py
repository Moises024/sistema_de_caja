from component.db import db
import sqlite3

def registrar_usuario(registrar,padre):
    nombre = registrar.input_nombre
    apellido = registrar.input_apellido
    contra = registrar.input_contra
    usuario = registrar.input_usuario
    array_input = [nombre,apellido,usuario,contra]
    
    for index,input in enumerate(array_input):
        if input.text() =='':
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Rellene el campo"
            padre.sendMsjWarningSingle(padre.tipo_msj)
            input.setFocus()
            return
        else:
             array_input[index] = input.text()

    #llamar data base
    baseDeDatos = db()
    conn = baseDeDatos.crearConnexion()
    cursor = conn.cursor()

    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE lower(nombre)=lower(?) and lower(apellido)=lower(?)",(array_input[0],array_input[1]))
        nombre = cursor.fetchone()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?",(array_input[2],))
        usuario = cursor.fetchone()
       
        if nombre:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Nombre/apellido existente"
            padre.sendMsjError(padre.tipo_msj)
            return
        
        if usuario:
            padre.tipo_msj.titulo = "Error"
            padre.tipo_msj.text = "Usuario ya existente"
            padre.sendMsjError(padre.tipo_msj)
            return
            
       
        cursor.execute("INSERT INTO usuarios(nombre,apellido,usuario,contra) VALUES(?, ?, ?, ?)",(array_input[0],array_input[1],array_input[2],array_input[3]))
        conn.commit()
    except sqlite3.Error as err:
       
        if err.sqlite_errorcode == 2067 :
            if err.args[0] == 'UNIQUE constraint failed: usuarios.contra':
                padre.tipo_msj.text = "Ingrese otra contraseña"
        else:
            padre.tipo_msj.text = "No se pudo crear el usuario"
        conn.close()
        padre.tipo_msj.titulo = "Error"
        padre.sendMsjError(padre.tipo_msj)
        return
    conn.close()


    padre.tipo_msj.titulo = "Éxito"
    padre.tipo_msj.text = "Usuario registrado correctamente"
    padre.sendMsjSuccess(padre.tipo_msj)
    
def conectar_acciones_registrar(registrar,padre):
    registrar.login.triggered.connect(lambda:padre.change_window(padre.login,7))
    registrar.salir.triggered.connect(padre.salir)

def conectar_botones_registrar(botones,registrar,padre):
    botones[0].clicked.connect(lambda:registrar_usuario(registrar,padre))
