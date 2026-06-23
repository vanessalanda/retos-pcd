# Reto Semana 7 — Extractor y Analizador de Logs

**Programación para Ciencia de Datos — IPN | Feb-Jul 2026**

## Descripción

Extractor y analizador de logs de servidor web usando expresiones regulares avanzadas. Parsea 4 tipos de logs, detecta amenazas de seguridad y genera un reporte completo.

## Características

- **Parsers** para logs HTTP, de errores, autenticación y base de datos
- **Detección de amenazas**: fuerza bruta, SQL injection, path traversal
- **Reporte** con estadísticas de acceso, errores y rendimiento
- **Bonus**: exportación a JSON, análisis temporal, detección de bots

## Uso

```bash
# Ejecutar directamente (los datos de prueba están incluidos en el script)
python main.py

# La salida incluye el reporte en consola y genera reporte.json
```

## Requisitos

- Python 3.6+
- Solo librerías estándar: `re`, `json`, `collections`

## Estructura

```
reto-semana-07/
├── main.py       # Solución completa
└── README.md
```

## Técnicas de Regex Usadas

- `(?P<nombre>...)` — grupos con nombre
- `re.VERBOSE` — patrones legibles con comentarios
- `(?<=...)` — lookbehind positivo
- `(?i)` — búsqueda sin distinción de mayúsculas/minúsculas
- `(?:...)` — grupos no capturantes
