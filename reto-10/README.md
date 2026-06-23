# Reto: Analizador de Precios de Acciones
**Asignatura:** Programación para Ciencia de Datos  
**Institución:** Instituto Politécnico Nacional (IPN)  
**Semestre:** Febrero - Julio 2026  

---

## 📌 Contexto del Problema
Una casa de bolsa requiere un sistema capaz de procesar y analizar el comportamiento histórico de precios de cierre de diferentes activos financieros utilizando la librería **Pandas (Series)** y **NumPy**. El objetivo principal del software es calcular métricas de rendimiento descritivas, identificar tendencias de mercado mediante indicadores técnicos y generar alertas de trading automatizadas para la toma de decisiones de inversión.
┌─────────────────────────────────────────────────────────────────────────┐
│                    ANALIZADOR DE ACCIONES                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ENTRADA                                                               │
│   ───────                                                               │
│   Series de precios de cierre diarios (Fechas como Índices)             │
│                                                                         │
│   ANÁLISIS                                                              │
│   ────────                                                              │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                  │
│   │Estadísticas │ → │ Rendimiento │ → │  Señales    │                  │
│   │  básicas    │   │  y riesgo   │   │  trading    │                  │
│   └─────────────┘   └─────────────┘   └─────────────┘                  │
│                                                                         │
│   SALIDA                                                                │
│   ──────                                                                │
│   • Reporte integral de rendimiento                                     │
│   • Bandas de Bollinger y Medias Móviles                                │
│   • Alertas de volatilidad y precio                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


---

## 🛠️ Estructura y Requerimientos Funcionales

El script principal está segmentado en tres componentes clave para cumplir de forma modular con la rúbrica de evaluación:

### Parte 1: Análisis Estadístico Básico (30%)
* **`estadisticas_basicas(precios)`**: Retorna un diccionario con métricas fundamentales del activo (precios máximos, mínimos, promedio, mediana, rango dinámico y días analizados).
* **`calcular_rendimientos(precios)`**: Determina el rendimiento diario porcentual aplicando transformaciones vectoriales de Pandas mediante `.pct_change()`.
* **`analisis_rendimientos(rendimientos)`**: Evalúa los comportamientos acumulados e identifica los hitos históricos (mejor y peor día con su respectiva fecha).

### Parte 2: Indicadores Técnicos (35%)
* **`media_movil(precios, ventana)`**: Calcula la media móvil simple (SMA) utilizando ventanas deslizantes con `.rolling()`.
* **`bandas_bollinger(precios, ventana, num_std)`**: Mide la dispersión estadística construyendo canales de volatilidad superiores e inferiores basados en desviaciones estándar.
* **`detectar_maximos_minimos(precios, ventana)`**: Identifica picos y valles locales comparando el valor actual frente a sus entornos vecinos.
* **`clasificar_tendencia(precios, ventana)`**: Evalúa si la trayectoria del precio actual se comporta de manera *ALCISTA*, *BAJISTA* o *LATERAL*.

### Parte 3: Sistema de Alertas (35%)
* **`generar_senales_trading(precios)`**: Modela una estrategia básica de cruce de medias móviles (corta de 5 días vs larga de 20 días) para disparar acciones de `COMPRA`, `VENTA` o `MANTENER`.
* **`alertas_precio(precios, umbral_cambio)`**: Filtra variaciones abruptas de precio que superen un porcentaje determinado de riesgo.
* **`clasificar_volatilidad(rendimientos)`**: Cataloga el nivel de riesgo del activo (Baja, Media, Alta, Muy Alta) según la desviación estándar de sus rendimientos.
* **`generar_reporte_completo(precios, nombre_accion)`**: Integra y consolida de forma unificada toda la metadata analizada para alimentar las vistas del usuario.

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
Asegúrate de contar con el entorno de Python configurado y las dependencias del curso instaladas en tu sistema local:

```bash
pip install pandas numpy