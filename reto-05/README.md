# Perfilador Universal de Datasets (Reto 05)

Este programa analiza automáticamente cualquier archivo CSV y genera un reporte de calidad de datos, identificando tipos de datos y problemas de valores faltantes.

## Estructura
- `main.py`: Lógica principal del perfilador.
- `data/`: Carpeta para colocar los datasets a analizar.
- `outputs/`: Carpeta donde se guardan los reportes generados.

## Instalación y Uso
1. Asegúrate de tener Python 3.8 o superior.
2. Crea y activa tu entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate