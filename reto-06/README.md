# Validador de Códigos con Expresiones Regulares (Reto 06)

## Descripción
Este sistema automatiza la validación de códigos logísticos para una empresa de distribución. Utiliza Expresiones Regulares para garantizar que los códigos de productos, envíos, empleados y facturas cumplan con los estándares internacionales y formatos internos de la empresa.

El programa no solo verifica el formato, sino que extrae los componentes esenciales de cada código (como categorías, fechas y números secuenciales) para su posterior procesamiento.

## Estructura del Proyecto

reto_semana_06/
│
├── main.py              # Ejecución del validador y procesamiento por lotes.
├── validador.py         # Lógica central con patrones Regex y validaciones.
├── requirements.txt     # (Sin dependencias externas)
└── README.md            # Documentación del proyecto.