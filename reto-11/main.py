import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

# =====================================================================
# PARTE 1: Carga y Exploración de Datos
# =====================================================================

def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carga los datos de estudiantes, calificaciones y materias.
    """
    estudiantes = pd.DataFrame({
        'boleta': ['2021630001', '2021630002', '2021630003', '2021630004', '2021630005',
                   '2022630001', '2022630002', '2022630003', '2022630004', '2022630005',
                   '2023630001', '2023630002', '2023630003', '2023630004', '2023630005'],
        'nombre': ['Juan Pérez García', 'María López Ruiz', 'Pedro Sánchez Torres',
                   'Ana Martínez Díaz', 'Luis Rodríguez Vega', 'Carmen Flores Luna',
                   'Roberto Díaz Mora', 'Laura Torres Silva', 'Diego Ramírez Cruz',
                   'Sofía Vargas Romo', 'Carlos Mendoza Ríos', 'Patricia Ortiz León',
                   'Miguel Ángel Castro', 'Fernanda Reyes Paz', 'Andrés Guzmán Villa'],
        'semestre': [4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2],
        'carrera': ['CD'] * 15,
        'email': ['juan.perez@ipn.mx', 'maria.lopez@ipn.mx', 'pedro.sanchez@ipn.mx',
                  'ana.martinez@ipn.mx', 'luis.rodriguez@ipn.mx', 'carmen.flores@ipn.mx',
                  'roberto.diaz@ipn.mx', 'laura.torres@ipn.mx', 'diego.ramirez@ipn.mx',
                  'sofia.vargas@ipn.mx', 'carlos.mendoza@ipn.mx', 'patricia.ortiz@ipn.mx',
                  'miguel.castro@ipn.mx', 'fernanda.reyes@ipn.mx', 'andres.guzman@ipn.mx']
    })
    
    materias = pd.DataFrame({
        'materia_id': ['MAT101', 'MAT102', 'PROG101', 'PROG102', 'EST101', 'EST102', 'BD101'],
        'nombre': ['Cálculo Diferencial', 'Cálculo Integral', 'Programación I',
                   'Programación II', 'Probabilidad', 'Estadística Inferencial',
                   'Bases de Datos'],
        'creditos': [8, 8, 6, 6, 6, 6, 6],
        'semestre_materia': [1, 2, 1, 2, 2, 3, 3]
    })
    
    np.random.seed(42)
    calificaciones_data = []
    
    for boleta in estudiantes['boleta']:
        semestre = estudiantes[estudiantes['boleta'] == boleta]['semestre'].values[0]
        materias_cursadas = materias[materias['semestre_materia'] <= semestre]['materia_id'].tolist()
        
        for materia in materias_cursadas:
            base = np.random.uniform(5, 10)
            p1 = round(min(10, max(0, base + np.random.normal(0, 1))), 1)
            p2 = round(min(10, max(0, base + np.random.normal(0, 1))), 1)
            final = round(min(10, max(0, base + np.random.normal(0, 0.5))), 1)
            
            if np.random.random() < 0.05:
                p2 = np.nan
            
            calificaciones_data.append({
                'boleta': boleta,
                'materia_id': materia,
                'parcial_1': p1,
                'parcial_2': p2,
                'final': final
            })
            
    # Forzar manualmente un par de alumnos en riesgo bajo los criterios exigidos
    # Miguel Ángel Castro (2023630003) -> Reprobarle materias
    calificaciones_data.append({'boleta': '2023630003', 'materia_id': 'MAT101', 'parcial_1': 5.0, 'parcial_2': 5.0, 'final': 5.0})
    calificaciones_data.append({'boleta': '2023630003', 'materia_id': 'PROG101', 'parcial_1': 4.0, 'parcial_2': 6.0, 'final': 5.0})
    # Luis Rodríguez Vega (2021630005) -> Promedio bajo
    for r in calificaciones_data:
        if r['boleta'] == '2021630005':
            r['parcial_1'] = 6.0; r['parcial_2'] = 6.0; r['final'] = 6.2
    
    calificaciones = pd.DataFrame(calificaciones_data).drop_duplicates(subset=['boleta', 'materia_id'], keep='last')
    return estudiantes, calificaciones, materias

def info_general(df_estudiantes: pd.DataFrame, df_calificaciones: pd.DataFrame) -> Dict:
    """
    Genera información general del sistema.
    """
    resultado = {
        "total_estudiantes": int(df_estudiantes['boleta'].nunique()),
        "total_registros_calif": int(len(df_calificaciones)),
        "semestres": sorted(list(df_estudiantes['semestre'].unique())),
        "materias_con_registros": int(df_calificaciones['materia_id'].nunique())
    }
    return resultado

def validar_datos(df_calificaciones: pd.DataFrame) -> Dict:
    """
    Valida la integridad de las columnas de calificaciones.
    """
    nulos = df_calificaciones.isna().any(axis=1).sum()
    
    # Comprobar fuera de rango (0 a 10) en parciales y finales
    fuera_rango = 0
    for col in ['parcial_1', 'parcial_2', 'final']:
        fuera_rango += ((df_calificaciones[col] < 0) | (df_calificaciones[col] > 10)).sum()
        
    resultado = {
        "registros_con_nulos": int(nulos),
        "calificaciones_fuera_rango": int(fuera_rango),
        "datos_validos": bool(fuera_rango == 0)
    }
    return resultado

# =====================================================================
# PARTE 2: Consultas y Filtros
# =====================================================================

def buscar_estudiante(df_estudiantes: pd.DataFrame, criterio: str, valor: str) -> pd.DataFrame:
    """
    Busca estudiantes filtrando por boleta, nombre o semestre.
    """
    if criterio == 'boleta':
        return df_estudiantes[df_estudiantes['boleta'] == valor]
    elif criterio == 'nombre':
        return df_estudiantes[df_estudiantes['nombre'].str.contains(valor, case=False, na=False)]
    elif criterio == 'semestre':
        return df_estudiantes[df_estudiantes['semestre'] == int(valor)]
    return pd.DataFrame()

def obtener_kardex(boleta: str, df_estudiantes: pd.DataFrame,
                   df_calificaciones: pd.DataFrame, df_materias: pd.DataFrame) -> Dict:
    """
    Genera el desglose académico (Kardex) para una boleta específica.
    """
    est_filtro = df_estudiantes[df_estudiantes['boleta'] == boleta]
    if est_filtro.empty:
        return {"estudiante": None, "materias": None, "promedio_general": 0.0, "creditos_cursados": 0, "materias_aprobadas": 0, "materias_reprobadas": 0}
        
    estudiante_dict = est_filtro.iloc[0].to_dict()
    calif_est = df_calificaciones[df_calificaciones['boleta'] == boleta].copy()
    
    # El promedio de cada materia se calcula promediando parcial_1, parcial_2 y final
    calif_est['promedio_materia'] = calif_est[['parcial_1', 'parcial_2', 'final']].mean(axis=1).round(2)
    
    # Unir con la información de la materia
    materias_unidas = pd.merge(calif_est, df_materias, on='materia_id', how='inner')
    
    # Procesar aprobados/reprobados (Aprobado >= 6.0)
    materias_unidas['aprobada'] = materias_unidas['promedio_materia'] >= 6.0
    
    aprobadas_df = materias_unidas[materias_unidas['aprobada'] == True]
    reprobadas_df = materias_unidas[materias_unidas['aprobada'] == False]
    
    prom_gral = materias_unidas['promedio_materia'].mean()
    if pd.isna(prom_gral): prom_gral = 0.0
    
    df_kardex_vista = materias_unidas[['materia_id', 'nombre', 'parcial_1', 'parcial_2', 'final', 'promedio_materia']]
    
    resultado = {
        "estudiante": estudiante_dict,
        "materias": df_kardex_vista,
        "promedio_general": float(round(prom_gral, 2)),
        "creditos_cursados": int(aprobadas_df['creditos'].sum()),
        "materias_aprobadas": int(len(aprobadas_df)),
        "materias_reprobadas": int(len(reprobadas_df))
    }
    return resultado

def filtrar_por_rendimiento(df_calificaciones: pd.DataFrame,
                            df_estudiantes: pd.DataFrame,
                            min_promedio: float = None,
                            max_promedio: float = None) -> pd.DataFrame:
    """
    Filtra estudiantes de acuerdo con su promedio general acumulado.
    """
    df_copia = df_calificaciones.copy()
    df_copia['prom_mat'] = df_copia[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    
    promedios_alumnos = df_copia.groupby('boleta')['prom_mat'].mean().reset_index()
    promedios_alumnos.columns = ['boleta', 'promedio']
    
    if min_promedio is not None:
        promedios_alumnos = promedios_alumnos[promedios_alumnos['promedio'] >= min_promedio]
    if max_promedio is not None:
        promedios_alumnos = promedios_alumnos[promedios_alumnos['promedio'] <= max_promedio]
        
    res = pd.merge(promedios_alumnos, df_estudiantes, on='boleta', how='inner')
    return res[['boleta', 'nombre', 'semestre', 'promedio']].round(2)

# =====================================================================
# PARTE 3: Cálculos y Estadísticas
# =====================================================================

def calcular_promedio_materia(df_calificaciones: pd.DataFrame, materia_id: str) -> Dict:
    """
    Calcula estadísticas e indicadores de aprobación de una materia.
    """
    calif_mat = df_calificaciones[df_calificaciones['materia_id'] == materia_id].copy()
    if calif_mat.empty:
        return {"materia": materia_id, "inscritos": 0, "promedio_general": 0.0, "tasa_aprobacion": 0.0}
        
    calif_mat['prom_mat'] = calif_mat[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    aprobados = (calif_mat['prom_mat'] >= 6.0).sum()
    
    resultado = {
        "materia": materia_id,
        "inscritos": int(len(calif_mat)),
        "promedio_parcial1": float(calif_mat['parcial_1'].mean()),
        "promedio_parcial2": float(calif_mat['parcial_2'].mean()),
        "promedio_final": float(calif_mat['final'].mean()),
        "promedio_general": float(round(calif_mat['prom_mat'].mean(), 2)),
        "tasa_aprobacion": float(round((aprobados / len(calif_mat)) * 100, 2)),
        "calificacion_maxima": float(calif_mat['prom_mat'].max()),
        "calificacion_minima": float(calif_mat['prom_mat'].min())
    }
    return resultado

def ranking_estudiantes(df_calificaciones: pd.DataFrame,
                        df_estudiantes: pd.DataFrame,
                        top_n: int = 10) -> pd.DataFrame:
    """
    Genera el top de alumnos ordenados por promedio.
    """
    df_copia = df_calificaciones.copy()
    df_copia['prom_mat'] = df_copia[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    
    promedios = df_copia.groupby('boleta')['prom_mat'].mean().reset_index()
    promedios.columns = ['boleta', 'Promedio']
    
    unido = pd.merge(promedios, df_estudiantes, on='boleta', how='inner')
    unido = unido.sort_values(by='Promedio', ascending=False).head(top_n).reset_index(drop=True)
    unido.index += 1
    unido = unido.reset_index().rename(columns={'index': 'Posición', 'nombre': 'Nombre', 'semestre': 'Semestre'})
    return unido[['Posición', 'Nombre', 'Semestre', 'Promedio']].round(2)

def estadisticas_por_semestre(df_estudiantes: pd.DataFrame,
                              df_calificaciones: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa los datos escolares calculando métricas por semestre de la carrera.
    """
    df_copia = df_calificaciones.copy()
    df_copia['prom_mat'] = df_copia[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    
    # Unir calificaciones con datos de estudiantes para conocer su semestre asignado
    unido = pd.merge(df_copia, df_estudiantes, on='boleta', how='inner')
    
    # Calcular promedios generales de cada alumno por separado
    alumnos_prom = unido.groupby(['semestre', 'boleta'])['prom_mat'].mean().reset_index()
    
    # Agrupar ahora por el nivel de semestre
    stats = alumnos_prom.groupby('semestre').agg(
        Estudiantes=('boleta', 'count'),
        Promedio=('prom_mat', 'mean')
    ).round(2)
    
    # Calcular tasa de aprobación global por semestre
    unido['aprobada'] = unido['prom_mat'] >= 6.0
    tasas = unido.groupby('semestre')['aprobada'].mean() * 100
    stats['Tasa Aprob.'] = tasas.round(1).astype(str) + '%'
    
    stats.index.name = 'Semestre'
    return stats

# =====================================================================
# PARTE 4: Identificación de Riesgo y Reportes
# =====================================================================

def identificar_estudiantes_riesgo(df_calificaciones: pd.DataFrame,
                                   df_estudiantes: pd.DataFrame,
                                   umbral_promedio: float = 7.0,
                                   max_reprobadas: int = 2) -> pd.DataFrame:
    """
    Identifica alumnos en riesgo basándose en el promedio general y materias reprobadas.
    """
    df_copia = df_calificaciones.copy()
    df_copia['prom_mat'] = df_copia[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    
    # Promedio e insuficiencias por alumno
    alumnos_stats = df_copia.groupby('boleta').agg(
        Promedio=('prom_mat', 'mean'),
        Reprobadas=('prom_mat', lambda x: (x < 6.0).sum())
    ).reset_index()
    
    riesgo_df = alumnos_stats[
        (alumnos_stats['Promedio'] < umbral_promedio) | 
        (alumnos_stats['Reprobadas'] >= max_reprobadas)
    ].copy()
    
    def definir_motivo(row):
        bajo_p = row['Promedio'] < umbral_promedio
        muchas_r = row['Reprobadas'] >= max_reprobadas
        if bajo_p and muchas_r: return "Ambos"
        if muchas_r: return "Mat. reprob."
        return "Bajo promedio"
        
    if riesgo_df.empty:
        return pd.DataFrame(columns=['Boleta', 'Nombre', 'Promedio', 'Reprobadas', 'Motivo'])
        
    riesgo_df['Motivo'] = riesgo_df.apply(definir_motivo, axis=1)
    
    res = pd.merge(riesgo_df, df_estudiantes, on='boleta', how='inner')
    res = res.rename(columns={'boleta': 'Boleta', 'nombre': 'Nombre', 'Promedio': 'Promedio', 'Reprobadas': 'Reprobadas'})
    return res[['Boleta', 'Nombre', 'Promedio', 'Reprobadas', 'Motivo']].round(2)

def generar_reporte_academico(df_estudiantes: pd.DataFrame,
                              df_calificaciones: pd.DataFrame,
                              df_materias: pd.DataFrame) -> Dict:
    """
    Consolida todas las analíticas en un único reporte.
    """
    df_copia = df_calificaciones.copy()
    df_copia['prom_mat'] = df_copia[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    
    prom_global = df_copia['prom_mat'].mean()
    tasa_aprob = (df_copia['prom_mat'] >= 6.0).mean() * 100
    
    reporte = {
        "resumen_general": {
            "total_estudiantes": int(len(df_estudiantes)),
            "promedio_global": float(round(prom_global, 2)),
            "tasa_aprobacion": float(round(tasa_aprob, 1))
        },
        "por_semestre": estadisticas_por_semestre(df_estudiantes, df_calificaciones),
        "mejores_estudiantes": ranking_estudiantes(df_calificaciones, df_estudiantes, top_n=5),
        "estudiantes_riesgo": identificar_estudiantes_riesgo(df_calificaciones, df_estudiantes),
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return reporte

def exportar_kardex(boleta: str, kardex: Dict, formato: str = 'csv') -> str:
    """
    Guarda el kardex generado en almacenamiento local (CSV o JSON).
    """
    fecha_str = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"kardex_{boleta}_{fecha_str}.{formato}"
    
    if kardex['materias'] is None:
        return "Error: Kardex vacío"
        
    if formato == 'csv':
        kardex['materias'].to_csv(nombre_archivo, index=False, encoding='utf-8')
    elif formato == 'json':
        datos_json = {
            "estudiante": kardex['estudiante'],
            "promedio_general": kardex['promedio_general'],
            "creditos_cursados": kardex['creditos_cursados'],
            "materias_aprobadas": kardex['materias_aprobadas'],
            "materias_reprobadas": kardex['materias_reprobadas'],
            "calificaciones": kardex['materias'].to_dict(orient='records')
        }
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, indent=4, ensure_ascii=False)
            
    return nombre_archivo

# =====================================================================
# VISUALIZACIONES COMPLEMENTARIAS
# =====================================================================

def mostrar_kardex(kardex: Dict) -> None:
    if kardex['estudiante'] is None:
        print("  Estudiante no encontrado")
        return
    est = kardex['estudiante']
    print("=" * 70)
    print("                         KARDEX ACADÉMICO")
    print("=" * 70)
    print(f"\n  DATOS DEL ESTUDIANTE")
    print("-" * 40)
    print(f"Boleta: {est.get('boleta', 'N/A')} | Nombre: {est.get('nombre', 'N/A')}")
    print(f"Semestre: {est.get('semestre', 'N/A')} | Carrera: {est.get('carrera', 'N/A')}")
    print(f"\n  CALIFICACIONES")
    print("-" * 70)
    print(kardex['materias'].to_string(index=False))
    print(f"\n  RESUMEN")
    print("-" * 40)
    print(f"Promedio General: {kardex.get('promedio_general', 0):.2f}")
    print(f"Créditos Cursados: {kardex.get('creditos_cursados', 0)}")
    print(f"Materias Aprobadas: {kardex.get('materias_aprobadas', 0)} | Reprobadas: {kardex.get('materias_reprobadas', 0)}")
    print("=" * 70)

def mostrar_reporte(reporte: Dict) -> None:
    print("=" * 70)
    print("              REPORTE ACADÉMICO - CIENCIA DE DATOS")
    print(f"              Generado: {reporte['fecha_generacion']}")
    print("=" * 70)
    res = reporte.get('resumen_general', {})
    print(f"\n  RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de estudiantes: {res.get('total_estudiantes', 'N/A')}")
    print(f"Promedio global: {res.get('promedio_global', 0):.2f}")
    print(f"Tasa de aprobación: {res.get('tasa_aprobacion', 0):.1f}%")
    
    print(f"\n  ESTADÍSTICAS POR SEMESTRE")
    print("-" * 40)
    print(reporte['por_semestre'].to_string())
    
    print(f"\n  TOP 5 ESTUDIANTES")
    print("-" * 40)
    print(reporte['mejores_estudiantes'].to_string(index=False))
    
    print(f"\n  ESTUDIANTES EN RIESGO")
    print("-" * 40)
    print(reporte['estudiantes_riesgo'].to_string(index=False))
    print("\n" + "=" * 70)

# =====================================================================
# EJECUCIÓN DEL SCRIPT
# =====================================================================

if __name__ == "__main__":
    df_estudiantes, df_calificaciones, df_materias = cargar_datos()
    print("DATOS CARGADOS CON ÉXITO.\n")
    
    print("INFORMACIÓN GENERAL")
    print(info_general(df_estudiantes, df_calificaciones))
    
    print("\nVALIDACIÓN DE DATOS")
    print(validar_datos(df_calificaciones))
    
    print("\nGENERANDO KARDEX DE PRUEBA (Boleta: 2021630001)...")
    kardex_alumno = obtener_kardex('2021630001', df_estudiantes, df_calificaciones, df_materias)
    mostrar_kardex(kardex_alumno)
    
    # Exportar archivo físico solicitado por el entregable
    archivo_csv = exportar_kardex('2021630001', kardex_alumno, formato='csv')
    print(f"  Archivo de Kardex exportado como: {archivo_csv}")
    
    print("\nEJECUTANDO REPORTE ACADÉMICO COMPLETO...")
    reporte_final = generar_reporte_academico(df_estudiantes, df_calificaciones, df_materias)
    mostrar_reporte(reporte_final)