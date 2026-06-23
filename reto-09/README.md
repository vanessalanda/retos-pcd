# Reto Semana 9 — SecureBank Fraud Detection

**Programación para Ciencia de Datos — IPN | Feb-Jul 2026**

## Descripción

Sistema de detección de anomalías en 2,500 transacciones bancarias (5 categorías × 500 transacciones) usando dos métodos estadísticos: IQR y Z-Score.

## Uso

```bash
# Instalar NumPy si no lo tienes
pip install numpy

# Ejecutar
python securebank.py
```

## Requisitos

- Python 3.7+
- NumPy (`pip install numpy`)

## Estructura

```
reto-semana-09/
├── securebank.py   # Solución completa
└── README.md
```

## Contenido por partes

| Parte | Contenido | Puntos |
|-------|-----------|--------|
| 1 | Estadísticas descriptivas, cuartiles, IQR, límites | 30 |
| 2 | Detección de outliers con método IQR | 25 |
| 3 | Cálculo de Z-Scores y detección con umbral \|z\| > 3 | 25 |
| 4 | Comparación de métodos + reporte ejecutivo | 20 |
| Bonus | Matriz de correlación entre categorías | +10 |

## Resultados obtenidos

- IQR detecta **71** transacciones anómalas (~2.8%)
- Z-Score detecta **55** transacciones anómalas (~2.2%)
- **55** transacciones coinciden en ambos métodos (alta prioridad)
- Los Z-Scores tienen media ~0 y std ~1 ✅

## Notas

- `np.random.seed(2024)` garantiza reproducibilidad
- No se usan loops para operaciones vectorizables
- Las anomalías inyectadas son ~3-5% del total, consistente con los resultados
