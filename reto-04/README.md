# Sistema de Gestión de Inventario Modular (Reto 04)

## Descripción
Este proyecto es una aplicación de consola desarrollada en Python que automatiza el control de stock de una tienda. El sistema lee un inventario desde un archivo CSV, identifica qué productos están por debajo de su nivel de stock mínimo y genera un reporte detallado con las unidades faltantes y el valor monetario del inventario actual.

Se aplicaron conceptos de **Programación Orientada a Objetos (POO)** y **Modularización** para separar la lógica de negocio, las validaciones y el manejo de archivos.

## Estructura del Proyecto
El código se organiza de forma modular para facilitar su mantenimiento:

reto-04/
├── main.py              # Punto de entrada y orquestación del programa.
├── README.md            # Documentación del proyecto.
├── models/
│   ├── __init__.py      # Define la carpeta como paquete.
│   └── producto.py      # Clase Producto (Atributos y métodos de cálculo).
├── utils/
│   ├── __init__.py      # Define la carpeta como paquete.
│   ├── io.py            # Funciones para lectura y escritura de archivos.
│   └── validators.py    # Lógica de validación de datos de entrada.
├── data/
│   └── inventario.csv   # Fuente de datos original.
└── outputs/
    └── reporte_inventario.csv  # Reporte generado de productos en reorden.