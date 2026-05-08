import re
from typing import Dict, List
from datetime import datetime

# Constantes de validación
DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']

def validar_producto(codigo: str) -> Dict:
    patron = r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$'
    match = re.match(patron, codigo)
    res = {"valido": False, "categoria": None, "numero": None, "pais": None}
    if match:
        res.update({"valido": True, "categoria": match.group(1), 
                    "numero": match.group(2), "pais": match.group(3)})
    return res

def validar_envio(codigo: str) -> Dict:
    patron = r'^ENV-(202[0-9]|2030)-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-(\d{6})$'
    match = re.match(patron, codigo)
    res = {"valido": False, "fecha": None, "secuencial": None}
    if match:
        try:
            # Validación de fecha real (Bonus)
            datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            res.update({"valido": True, "fecha": f"{match.group(1)}-{match.group(2)}-{match.group(3)}", 
                        "secuencial": match.group(4)})
        except ValueError: pass
    return res

def validar_empleado(codigo: str) -> Dict:
    patron = r'^EMP-([A-Z]{3})-([1-9]\d{3})$'
    match = re.match(patron, codigo)
    res = {"valido": False, "departamento": None, "numero": None}
    if match and match.group(1) in DEPARTAMENTOS_VALIDOS:
        res.update({"valido": True, "departamento": match.group(1), "numero": match.group(2)})
    return res

def validar_factura(codigo: str) -> Dict:
    patron = r'^FAC-([A-E])-(\d{6})$'
    match = re.match(patron, codigo)
    res = {"valido": False, "serie": None, "numero": None}
    if match:
        res.update({"valido": True, "serie": match.group(1), "numero": match.group(2)})
    return res

def validar_codigo(codigo: str) -> Dict:
    resultado = {"codigo": codigo, "tipo": "desconocido", "valido": False, "detalles": {}}
    if codigo.startswith("ENV-"):
        resultado["tipo"], res_val = "envio", validar_envio(codigo)
    elif codigo.startswith("EMP-"):
        resultado["tipo"], res_val = "empleado", validar_empleado(codigo)
    elif codigo.startswith("FAC-"):
        resultado["tipo"], res_val = "factura", validar_factura(codigo)
    else:
        res_val = validar_producto(codigo)
        resultado["tipo"] = "producto" if (res_val["valido"] or "-" in codigo) else "desconocido"
    
    resultado["valido"] = res_val.pop("valido")
    resultado["detalles"] = res_val
    return resultado

def procesar_lote(codigos: List[str]) -> Dict:
    reporte = {
        "total": len(codigos), "validos": 0, "invalidos": 0,
        "por_tipo": {t: {"total": 0, "validos": 0} for t in ["producto", "envio", "empleado", "factura", "desconocido"]},
        "detalle": []
    }
    for cod in codigos:
        res = validar_codigo(cod)
        reporte["detalle"].append(res)
        reporte["por_tipo"][res["tipo"]]["total"] += 1
        if res["valido"]:
            reporte["validos"] += 1
            reporte["por_tipo"][res["tipo"]]["validos"] += 1
        else:
            reporte["invalidos"] += 1
    return reporte

CODIGOS_PRUEBA = [
    "TEC-0001-MX", "ALI-9999-US", "ROB-1234-CA", "tec-0001-MX", "TEC-001-MX", "TECH-0001-MX",
    "ENV-2024-03-15-001234", "ENV-2025-12-01-999999", "ENV-2019-03-15-001234", "ENV-2024-13-15-001234", "ENV-2024-03-32-001234",
    "EMP-VEN-1234", "EMP-TEC-9999", "EMP-ADM-1000", "EMP-VEN-0123", "EMP-XXX-1234", "EMP-VEN-123",
    "FAC-A-123456", "FAC-E-000001", "FAC-B-999999", "FAC-F-123456", "FAC-A-12345", "FAC-a-123456",
    "XXX-1234", "RANDOM-CODE"
]