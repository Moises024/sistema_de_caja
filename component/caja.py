
class tecla:
   valor=""
keys = tecla()

def teclado(caja):
    valor = caja.sender().text()
    if int(valor) >= 50:
      keys.valor = valor
    else:
        keys.valor += valor

    caja.monto_pagado.setText(keys.valor)

def back(caja):
    keys.valor= keys.valor[:-1]
    caja.monto_pagado.setText(keys.valor)

def devuelta(caja,padre):
   if caja.precio_total.text() == "" or caja.monto_pagado.text() == "":
        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = f"No se puede hacer dicha operación"
        padre.sendMsjWarning(padre.tipo_msj)
        return
   precio_total = int(caja.precio_total.text())
   monto_pagado = int(caja.monto_pagado.text())
   if monto_pagado < precio_total:
        msj = precio_total - monto_pagado
        padre.tipo_msj.titulo = "Warning"
        padre.tipo_msj.text = f"Faltan {msj} pesos por cobrar"
        padre.sendMsjWarning(padre.tipo_msj)
        return
   monto_devolver = (precio_total - monto_pagado ) * -1
   caja.devuelta_2.setText(str(monto_devolver))
def conectar_botones_caja(botones,padre,login,caja):
 botones[0].clicked.connect( lambda:padre.change_window(login,0))
 botones[1].clicked.connect(lambda:teclado(caja))
 botones[2].clicked.connect(lambda:teclado(caja))
 botones[3].clicked.connect(lambda:teclado(caja))
 botones[4].clicked.connect(lambda:teclado(caja))
 botones[5].clicked.connect(lambda:teclado(caja))
 botones[6].clicked.connect(lambda:teclado(caja))
 botones[7].clicked.connect(lambda:teclado(caja))
 botones[8].clicked.connect(lambda:teclado(caja))
 botones[9].clicked.connect(lambda:teclado(caja))
 botones[10].clicked.connect(lambda:teclado(caja))
 botones[11].clicked.connect(lambda:teclado(caja))
 botones[12].clicked.connect(lambda:teclado(caja))
 botones[13].clicked.connect(lambda:teclado(caja))
 botones[14].clicked.connect(lambda:teclado(caja))
 botones[15].clicked.connect(lambda:teclado(caja))
 botones[16].clicked.connect(lambda:teclado(caja))
 botones[17].clicked.connect(lambda:teclado(caja))
 botones[18].clicked.connect(lambda:back(caja))
 botones[19].clicked.connect(lambda:devuelta(caja,padre))

def conectar_acciones_caja(acciones,padre):
    acciones[0].triggered.connect(padre.salir)