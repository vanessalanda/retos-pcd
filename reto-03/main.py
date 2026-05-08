# Reto semana 03
print ("Reto 3")
import sys
def manin ():
    #diccionario principal 
    productos = {}
    
    primera_linea = True
    
    #se lee linea por linea
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        if primera_linea:
            primera_linea = False
            continue
        partes = linea.split(",")
        if len(partes) !=4:
            continue
        
        producto = partes[1].strip()
        
        try:
            cantidad = int(partes[2])
            precio_unitario = float(partes[3])
        except ValueError:
            continue
            
        