import os

def leer_inventario(ruta_archivo):
    """
    Lee el archivo CSV y devuelve una lista de diccionarios.
    """
    productos_raw = []
    
    # Verificamos si el archivo existe antes de intentar abrirlo
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo en {ruta_archivo}")
        return productos_raw
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        
        if not lineas:
            return productos_raw
        
        # Obtenemos los nombres de las columnas de la primera línea
        encabezados = lineas[0].strip().split(',')
        
        for linea in lineas[1:]:
            linea = linea.strip()
            if not linea:
                continue
            
            valores = linea.split(',')
            # Solo procesamos si la fila tiene el número correcto de columnas
            if len(valores) == len(encabezados):
                producto_dict = dict(zip(encabezados, valores))
                productos_raw.append(producto_dict)
    
    return productos_raw

def escribir_reporte(productos, ruta_archivo):
    """
    Guarda los productos que necesitan reorden en un nuevo CSV.
    """
    # Si no existe la carpeta 'outputs', el programa la crea solita
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    
    encabezados = [
        "sku", "nombre", "categoria", "stock_actual", 
        "stock_minimo", "unidades_faltantes", "valor_inventario"
    ]
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos la primera fila (títulos)
        archivo.write(','.join(encabezados) + '\n')
        
        # Escribimos cada producto que necesita piezas
        for p in productos:
            linea = [
                str(p.sku),
                str(p.nombre),
                str(p.categoria),
                str(p.stock),
                str(p.stock_minimo),
                str(p.unidades_faltantes()),
                f"{p.valor_inventario():.2f}"
            ]
            archivo.write(','.join(linea) + '\n')