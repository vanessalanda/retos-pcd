from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

def main():
    print("--- Iniciando Sistema de Inventario ESCOM ---")
    
    # 1. Leer los datos del archivo CSV
    ruta_entrada = "data/inventario.csv"
    datos_raw = leer_inventario(ruta_entrada)
    
    if not datos_raw:
        print("Advertencia: No se encontraron datos en el archivo o el archivo no existe.")
        return

    # 2. Convertir los datos a objetos de la clase Producto y validar
    productos_validos = []
    for datos in datos_raw:
        # Intentamos validar cada fila del CSV
        valido, error = validar_producto(
            datos.get('sku'), datos.get('nombre'), datos.get('categoria'),
            datos.get('precio'), datos.get('stock'), datos.get('stock_minimo')
        )
        
        if valido:
            p = Producto(
                datos['sku'], datos['nombre'], datos['categoria'],
                float(datos['precio']), int(datos['stock']), int(datos['stock_minimo'])
            )
            productos_validos.append(p)
        else:
            print(f"Fila ignorada por error: {error}")

    # 3. Filtrar solo los que necesitan reorden (stock < stock_minimo)
    necesitan_reorden = [p for p in productos_validos if p.necesita_reorden()]
    
    # 4. Ordenar por urgencia (el que más piezas le falten va primero)
    necesitan_reorden.sort(key=lambda x: x.unidades_faltantes(), reverse=True)
    
    # 5. Generar el archivo de salida
    ruta_salida = "outputs/reporte_inventario.csv"
    escribir_reporte(necesitan_reorden, ruta_salida)
    
    print("\n=== RESUMEN DEL PROCESO ===")
    print(f"Productos leídos correctamente: {len(productos_validos)}")
    print(f"Productos que requieren reorden: {len(necesitan_reorden)}")
    print(f"Reporte generado en: {ruta_salida}")
    print("===========================")

if __name__ == "__main__":
    main()