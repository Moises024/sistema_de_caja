
import re
def formatearDigitos(valor):
    valor_str = str(valor)[::-1]
    nuevo_string =""
    for i,v in enumerate(valor_str):
        if i % 3 ==0 and i !=0:
            nuevo_string += ","
        nuevo_string +=v 
    return nuevo_string[::-1]

def format_us(number):
    # quitar todo lo que no sea dígito
    digits = re.sub(r'\D', '', number)
    if len(digits) != 10:
        return number  # devuelvo original si no tiene 10 dígitos
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"