#calculadora de sumas semana 01

def limpiar_valor(valor):
    valor = valor.strip()
    
    if valor == "":
        return 0
    
    numero = ""
    punto_encontrado = False
    
    for c in valor:
        if c.isdigit():
            numero += c
        elif c == "." and not punto_encontrado:
            punto_encontrado = True
            break
        else:
            break
    
    if numero == "":
        return 0

    return int(numero)

#programa principal
linea = input("Ingresa numeros separados por comas: ")
valores = linea.split(",")

suma = 0

for v in valores:
    suma += limpiar_valor(v)
    
print("La suma total es:", suma)
