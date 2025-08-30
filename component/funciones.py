
def formatearDigitos(valor):
    valor_str = str(valor)[::-1]
    nuevo_string =""
    for i,v in enumerate(valor_str):
        if i % 3 ==0 and i !=0:
            nuevo_string += ","
        nuevo_string +=v 
    return nuevo_string[::-1]
