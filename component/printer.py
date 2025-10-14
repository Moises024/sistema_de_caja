import win32print
from datetime import datetime
import json
from component.funciones import format_us

def printer(data,flags=True):
    print("imprimiendo..")
    facturas = json.loads(data["factura"])
    devuelta = str(data["devuelta"]).encode()
    recibido = str(data["recibido"]).encode()
    no_factura = str(data["no_factura"]).encode()
    vendedor = data["usuario"].encode()
    cliente = data["cliente"].encode()
    devoluciones = b"No aceptamos devoluciones de pacas ya abiertas"
    printer_name = "POS80 Printer"  # ← cámbialo por el nombre exacto de tu impresora
    CENTER = b'\x1B\x61\x01'
    LEFT = b'\x1B\x61\x00'
    RIGHT = b'\x1B\x61\x02'
    BIG = b'\x1D\x21\x11'     # Texto grande (x2 alto y ancho)
    NORMAL = b'\x1D\x21\x00'  # Texto normal
    ESPACIOS = b"\x1B\x64\x05"
    direccion = b"Calle Padre Fantino Frente al Parque De "
    direccion_ = b"Las Delicias en Plaza Luna, Bonao."
    telefono = b"809-603-8368"
    hora = str(datetime.now().hour).encode()
    min = str(datetime.now().minute).encode()
    fecha = str(datetime.now().date()).encode()
    sector = str(data["sector"]).encode()
    tel = str(format_us(data["telefono"])).encode()

    raw_text =   (ESPACIOS+
        CENTER + BIG +
        b"Pacas Bonao" + b"\n"*2+

        NORMAL+
        direccion +b"\n" +
        direccion_ + b"\n" +
        b"TEL: " +telefono + b"\n"+
        NORMAL + LEFT + b"\n"*2 +
        b"Factura: " + no_factura +b"\n" +
        b"Fecha: "+fecha  + b" "*2 + b"Hora: " +hora+b":"+min+
        b"\n"*2 +
        b"----------------------"  * 2 + b"\n" +
        b"Cliente:  " + cliente + b"\n" +
        b"Sector: " +sector + b"\n" +
        b"Tel:  " + tel + b"\n" +
        b"----------------------"  * 2 + b"\n" +
        b"Vendedor: " + vendedor + b"\n" +
        b"----------------------"  * 2 + b"\n" +
        b"------ ------ ------ --------" + b"\n"+
        b" CANT. "+b"PRECIO. "+b"DESC. "+b"IMPORTE. " +b"\n"+
        b"------ ------ ------ --------" + b"\n"
        )
    total = str(data["total"]).encode()
    for factura in facturas:
        try:
            nombre = factura["nombre"]
            precio = factura["precio"]
            descuento = factura["descuento"]
            cant = factura["cantidad"]
            raw_text +=( nombre.encode("utf-8") + b"\n"+
                       str(cant).encode("utf-8") + b" "*6+
                         b"$" +str(precio).encode("utf-8")+b".00" + b" "*6+
                         b"$" +str(descuento).encode("utf-8")+b".00" +  b" "*6+
                         b"$" +str(factura["total"]).encode("utf-8")+b".00" + b"\n"
                         )
            
        except Exception as e:
            print(e)
            pass

    raw_text +=(
        b"\n" * 3 +
        LEFT + b"Total: "+ b"$"+ total + b".00" + b"\n"+
        LEFT+
                b"----------------------"  * 2 + b"\n" +
                b"Recibido:  " + b"$" + recibido + b".00"                 + b"\n" +
                b"Devuelta:  " + b"$" + devuelta + b".00"              + b"\n" +
                b"----------------------"  * 2 + b"\n" 
                
                )
    raw_text += (CENTER +b"\n" + devoluciones + b"\n"*2 ) #cortar papelrw
    if flags:
        raw_text += (CENTER +b"\n" + b"ORIGINAL" + b"\n"*2 )
    else:
       raw_text += (CENTER +b"\n" + b"COPIA" + b"\n"*2 )
    raw_text += (b"Gracias por su compra!!\n" +
        b"\x1D\x56\x00")
    
 
    # Abrir impresora
    hprinter = win32print.OpenPrinter(printer_name)
    job = win32print.StartDocPrinter(hprinter, 1, ("Ticket Python", None, "RAW"))
    win32print.StartPagePrinter(hprinter)
    win32print.WritePrinter(hprinter, raw_text)
    win32print.EndPagePrinter(hprinter)
    win32print.EndDocPrinter(hprinter)
    win32print.ClosePrinter(hprinter)
# data = {
#     "factura":'[{"nombre":"Picapollo","precio":100,"cantidad":1,"total":100,"descuento":0},{"nombre":"Picapollo","precio":100,"cantidad":1,"total":100,"descuento":0}]',
#     "total":200,
#     "devuelta":300,
#     "recibido":500,
#     "no_factura":23,
#     "usuario":"Deivi",
#     "cliente":"Richie",
#     "sector":"BONAO",
#     "telefono":"8095253681"
# }
# printer(data, True)