# Reto 03: Analizador de Ventas de Tecnología

Este programa es un procesador de transacciones para una tienda, lo que hace es agarrar un montón de ventas sueltas y juntarlas por producto para saber cuánto se vendió en total, cuánto dinero entró y cuál fue el precio promedio.

## ¿Qué hace el script?
1. Agrupa todo: Si vendiste 5 Laptops el lunes y 2 el martes, el programa te saca el total de 7 en una sola fila.
2. Calcula el dinero: Multiplica la cantidad por el precio de cada venta y lo va sumando.
3. Ordena por lana: El reporte siempre pone hasta arriba el producto que dejó más dinero (orden descendente).
4. Limpia errores: Si una línea viene mocha o con letras donde no debe, simplemente la ignora para no romper el programa.

## ¿Cómo se usa?
Igual que el reto pasado, funciona con tuberías desde la terminal. 

type ventas.csv | python main.py

