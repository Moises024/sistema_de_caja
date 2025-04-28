
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
    botones[9].clicked.connect(lambda:padre.teclado9(9,login)) 
    botones[10].clicked.connect(lambda:padre.userValidate(login,caja))
    botones[11].clicked.connect(lambda:padre.borrar(login))


def conectar_acciones_login(login,padre):
    login.salir.triggered.connect(padre.salir)
    

