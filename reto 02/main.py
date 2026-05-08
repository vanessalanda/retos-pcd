# Reto semana 2 clasificador de temperaturas

import sys

def fahrenheit_a_celsius(f):
    """
    Regla 1: Convierte Fahrenheit a Celsius usando la formula:
    (F-32) * 5/9
    """
    return (f-32) * 5/9

def clasificar_temperatura(celsius):
    """
    Regla 2: Clasifica la temperatura segun los rangos establecidos:
    - < 0:Congelante
    - 0 a 15: Frio
    - 16 a 25: Templado
    - 26 a 35: Calido
    - >35: Extremo
    """
    if celsius < 0:
        return "Congelante"
    elif celsius <= 15: #del 0 al 15
        return "Frio"
    elif celsius <= 25: #del 16 al 25
        return "Templado"
    elif celsius <=35: #del 26 al 35
        return "Calido"
    else: #mayor a 35
        return "Extremo"
    
def main():
    #imprime encabezados de salida
    print("Ciudad, Temperatura_celsius, Clasificacion")
    
    primera_linea = True
    
    #procesar desde stdin
    
    for linea in sys.stdin:
        linea = linea.strip()
        
        if not linea: #lineas vacias
            continue
        
        if primera_linea: #omitir la primera linea de encabezado
            primera_linea = False
            continue
        partes = linea.split (",")
        if len(partes) != 3:
            continue
        ciudad = partes[0].strip()
        temp_str = partes [1].strip()
        unidad = partes[2].strip().upper()
        
        #validar unidad sea C o F
        if unidad  not in ["C", "F"]:
            continue
        
        #validar que la temperatura respete los rangos 
        try:
            temperatura_original = float(temp_str)
        except ValueError:
            continue
        
        #realizar conversion
        if unidad == "F":
            celsius = fahrenheit_a_celsius(temperatura_original)
        else:
            celsius = temperatura_original
            
            #clasificacion
        categoria = clasificar_temperatura(celsius)
        #formato de salida
        print(f"{ciudad},{celsius:.1f},{categoria}")
        
    if __name__ == "__main__":
        main()