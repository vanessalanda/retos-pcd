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
        if producto not in productos:
            
            productos[producto] = {
                "unidaes": 0,
                "ingreso": 0.0
            }
            
        productos[producto]["unidades"] += cantidad
        productos[producto]["ingreso"] += cantidad * precio_unitario
        
        
        
    reporte_final = []
    for nombre, datos in productos.items():
        unidades = datos["unidades"]
        ingreso = datos["ingreso"]
        
        promedio = ingreso / unidades if unidades > 0 else 0
        
        reporte_final.append({
            "producto": nombre,
            "unidades": unidades, 
            "ingreso": ingreso, 
            "promedio": promedio
        })
        
    reporte_ordenado = sorted(
        reporte_final,
        key=lambda x: x["Ingreso"],
        reverse=True
    )
    
    print("Producto,unidades_vendidas,ingreso_total,precio_promedio")
    for p in reporte_ordenado:
        
        print(f"{p['producto']},{p['unidades']},{p['ingreso']:.2f},{p['promedio']:.2f}")
        
if __name__=="__main__":
    main()
            
            
        