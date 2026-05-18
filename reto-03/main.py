# Reto semana 03

import sys

def main():
    # Diccionario para agrupar por producto
    productos = {}
    
    primera_linea = True
    
    # Leer todas las líneas desde stdin
    for linea in sys.stdin:
        linea = linea.strip()
        
        # Saltar el encabezado obligatorio: fecha,producto,cantidad,precio_unitario
        if primera_linea:
            primera_linea = False
            continue
            
        # Regla 5: Saltar líneas completamente vacías
        if not linea:
            continue
            
        
        partes = linea.split(',')
        
        
        if len(partes) != 4:
            continue  
            
        fecha = partes[0]
        producto = partes[1].strip()
        
        
        try:
            cantidad = int(partes[2])
            precio = float(partes[3])
        except ValueError:
            continue  # Ignorar la línea si no contiene números válidos
            
        
        if producto not in productos:
            productos[producto] = {
                "unidades": 0,
                "ingreso": 0.0
            }
            
        # Regla 1 y 2: Acumular las unidades vendidas y el ingreso total (cantidad * precio)
        productos[producto]["unidades"] += cantidad
        productos[producto]["ingreso"] += cantidad * precio
        
    # Regla 2: Calcular el precio promedio para cada producto consolidado
    for prod in productos:
        unidades = productos[prod]["unidades"]
        ingreso = productos[prod]["get_ingreso"] = productos[prod]["ingreso"]
        # Evitar división por cero si existiera algún caso raro
        productos[prod]["promedio"] = ingreso / unidades if unidades > 0 else 0
        
    # Regla 3: Ordenar por ingreso total de forma descendente (reverse=True)
    productos_ordenados = sorted(
        productos.items(),
        key=lambda x: x[1]["ingreso"],
        reverse=True
    )
    
    # Regla 4: Especificación de Salida Estricta en CSV
    print("producto,unidades_vendidas,ingreso_total,precio_promedio")
    for nombre, datos in productos_ordenados:
        unidades = datos["unidades"]
        ingreso = datos["ingreso"]
        promedio = datos["promedio"]
        # Formato de números: unidades como entero, montos con 2 decimales (.2f)
        print(f"{nombre},{unidades},{ingreso:.2f},{promedio:.2f}")

if __name__ == "__main__":
    main()