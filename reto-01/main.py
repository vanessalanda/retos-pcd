import sys

def limpiar_valor(valor: str) -> str:
    """
    Elimina espacios y caracteres no permitidos (solo deja dígitos, '.' y '-').
    Regla 5 y 6.
    """
    caracteres_validos = '0123456789.-'
    # Quitamos espacios y filtramos caracteres
    limpio = "".join(char for char in valor.strip() if char in caracteres_validos)
    return limpio

def convertir_y_truncar(valor_limpio: str) -> int:
    """
    Convierte a float y trunca a entero. 
    Maneja valores vacíos o mal formados retornando 0.
    Regla 2 y 4.
    """
    if not valor_limpio or valor_limpio == "." or valor_limpio == "-":
        return 0
    try:
        # float() maneja casos como "-0.5" o ".5"
        # int() sobre un float trunca hacia el cero (Regla 4)
        return int(float(valor_limpio))
    except ValueError:
        return 0

def procesar_linea(linea: str) -> int:
    """
    Procesa la línea completa separando por comas y sumando resultados.
    Regla 1 y 3.
    """
    # Si la línea está vacía o solo tiene espacios (Regla 1)
    if not linea.strip():
        return 0
    
    # Separar por comas
    partes = linea.split(',')
    suma_total = 0
    
    for parte in partes:
        limpio = limpiar_valor(parte)
        numero = convertir_y_truncar(limpio)
        suma_total += numero
        
    return suma_total

def main():
    """
    Punto de entrada: Lee de stdin y escribe en stdout.
    """
    for linea in sys.stdin:
        # El profesor pide exactamente el resultado por línea
        resultado = procesar_linea(linea)
        sys.stdout.write(f"{resultado}\n")

if __name__ == "__main__":
    main()