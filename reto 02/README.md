# Reto 02: Clasificador de Clima (Semana 2)

Este es mi proyecto de la segunda semana, la idea es recibir una lista de ciudades con temperaturas mezcladas (unas en Celsius y otras en Fahrenheit) y sacar un reporte limpio donde todo esté en Celsius y nos diga qué tipo de clima tiene cada una.

## ¿Qué hace el programa?
1. Limpia los datos: Si una linea viene mal, le falta una columna o la temperatura no es un número, el programa la ignora y sigue con la que sigue
2. Convierte a Celsius: Si detecta que la unidad es fahrenheit, aplica la fórmula para pasarla a C
3. Clasifica: Dependiendo de los grados, le asigna una etiqueta:
   * Menos de 0: Congelante
   * 0 a 15: Frio
   * 16 a 25: Templado
   * 26 a 35: Calido
   * Más de 35: Extremo
4. **Formato:** Al final todo sale con un solo decimal para que se vea ordenado.

## Cómo correrlo
Como el programa lee desde la entrada estándar, lo mejor es usar un archivo de texto con los datos y mandárselo así en la terminal:

type entrada.txt | python main.py