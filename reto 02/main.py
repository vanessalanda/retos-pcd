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
    
        