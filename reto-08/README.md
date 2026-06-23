# Reto Semana 8 — MeteoSense Analytics

**Programación para Ciencia de Datos — IPN | Feb-Jul 2026**

## Descripción

Sistema de análisis de datos meteorológicos con NumPy. Procesa mediciones de temperatura, humedad y CO2 de 5 estaciones en CDMX durante 7 días.

## Uso

```bash
# Instalar NumPy si no lo tienes
pip install numpy

# Ejecutar
python meteosense.py
```

## Requisitos

- Python 3.7+
- NumPy (`pip install numpy`)

## Estructura

```
reto-semana-08/
├── meteosense.py   # Solución completa
└── README.md
```

## Temas cubiertos

| Parte | Contenido | Puntos |
|-------|-----------|--------|
| 1 | Exploración: ndim, shape, dtype, indexación, slicing | 25 |
| 2 | Estadísticas: nanmean, nanmax, nanstd por ejes | 25 |
| 3 | Operaciones vectorizadas, broadcasting, ICT | 25 |
| 4 | Detección de anomalías, análisis de contingencia | 25 |
| Bonus | Reporte ejecutivo completo | +10 |

## Notas

- Se usa `np.random.seed(42)` para reproducibilidad — los resultados son siempre los mismos
- Todas las operaciones usan funciones `nan*` para manejar valores faltantes
- **No se usan loops** en las partes 2, 3 y 4 — todo es vectorizado
