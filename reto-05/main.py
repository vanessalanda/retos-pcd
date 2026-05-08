#codigo principal
import argparse
import sys
import os

def es_valor_nulo(valor):
    if valor is None:
        return True
    if isinstance(valor, str) and valor.strip() == "":
        return True
    return False

def es_numerico(valor):
    try:
        float(str(valor).replace(',', '').strip())
        return True
    except (ValueError, TypeError):
        return False

def es_fecha(valor):
    v = str(valor).strip()
    if len(v) >= 10 and v[4] == '-' and v[7] == '-':
        try:
            partes = v[:10].split('-')
            año, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
            return 1900 <= año <= 2100 and 1 <= mes <= 12 and 1 <= dia <= 31
        except (ValueError, IndexError):
            pass
    return False

def es_booleano(valor):
    v = str(valor).strip().lower()
    return v in ['true', 'false', 'yes', 'no', 'si', '1', '0', 't', 'f']

def inferir_tipo(valores):
    valores_validos = [v for v in valores if not es_valor_nulo(v)]
    if not valores_validos:
        return "texto"
    
    total = len(valores_validos)
    umbral = 0.8
    
    num_fechas = sum(1 for v in valores_validos if es_fecha(v))
    num_booleanos = sum(1 for v in valores_validos if es_booleano(v))
    num_numericos = sum(1 for v in valores_validos if es_numerico(v))
    
    if num_fechas / total >= umbral:
        return "fecha"
    elif num_booleanos / total >= umbral:
        return "booleano"
    elif num_numericos / total >= umbral:
        return "numerico"
    else:
        return "texto"

def perfilar_columna(nombre, valores):
    total = len(valores)
    nulos = sum(1 for v in valores if es_valor_nulo(v))
    valores_no_nulos = [v for v in valores if not es_valor_nulo(v)]
    unicos = len(set(valores_no_nulos))
    ejemplo = valores_no_nulos[0] if valores_no_nulos else ""
    tipo = inferir_tipo(valores)
    
    pct_nulos = round((nulos / total) * 100, 2) if total > 0 else 0.00
    pct_unicos = round((unicos / total) * 100, 2) if total > 0 else 0.00
    
    return {
        "nombre_columna": nombre,
        "tipo_inferido": tipo,
        "total_registros": total,
        "valores_nulos": nulos,
        "porcentaje_nulos": pct_nulos,
        "valores_unicos": unicos,
        "porcentaje_unicos": pct_unicos,
        "ejemplo_valor": ejemplo
    }

def main():
    parser = argparse.ArgumentParser(description="Perfilador Universal de Datasets CSV")
    parser.add_argument("--input", "-i", required=True, help="Ruta al CSV de entrada")
    parser.add_argument("--output", "-o", required=True, help="Ruta al CSV de salida")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: El archivo {args.input} no existe.")
        sys.exit(1)

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            lineas = [l.strip() for l in f.readlines() if l.strip()]
        
        if not lineas:
            print("Error: El archivo está vacío.")
            return

        encabezados = lineas[0].split(',')
        filas = [l.split(',') for l in lineas[1:]]
        
        perfiles = []
        for i, nombre_col in enumerate(encabezados):
            valores = [f[i] if i < len(f) else "" for f in filas]
            perfiles.append(perfilar_columna(nombre_col, valores))

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        
        columnas_out = ["nombre_columna","tipo_inferido","total_registros","valores_nulos","porcentaje_nulos","valores_unicos","porcentaje_unicos","ejemplo_valor"]
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(",".join(columnas_out) + "\n")
            for p in perfiles:
                linea = [
                    str(p["nombre_columna"]), p["tipo_inferido"], str(p["total_registros"]),
                    str(p["valores_nulos"]), f"{p['porcentaje_nulos']:.2f}",
                    str(p["valores_unicos"]), f"{p['porcentaje_unicos']:.2f}",
                    str(p["ejemplo_valor"])
                ]
                f.write(",".join(linea) + "\n")
        
        print(f"Éxito: Perfil generado en {args.output}")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()