import win32print

printer_name = "POS80 Printer"  # ← cámbialo por el nombre exacto de tu impresora

raw_text = b"""
TICKET DE PRUEBA
---------------------
Producto A      $12.00
Producto B      $18.00
TOTAL           $30.00

Gracias por su compra!
\x1D\x56\x00  # Comando para cortar papel
"""

# Abrir impresora
hprinter = win32print.OpenPrinter(printer_name)
job = win32print.StartDocPrinter(hprinter, 1, ("Ticket Python", None, "RAW"))
win32print.StartPagePrinter(hprinter)
win32print.WritePrinter(hprinter, raw_text)
win32print.EndPagePrinter(hprinter)
win32print.EndDocPrinter(hprinter)
win32print.ClosePrinter(hprinter)