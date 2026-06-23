 import re
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict


# ══════════════════════════════════════════════════════════════════
#                    PARTE 1: PARSERS DE LOGS
# ══════════════════════════════════════════════════════════════════

PATRON_HTTP = re.compile(r'''
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})   # Dirección IP
    \s+-\s+-\s+                          # Guiones de usuario/auth
    \[(?P<timestamp>[^\]]+)\]            # Timestamp entre corchetes
    \s+"(?P<method>[A-Z]+)              # Método HTTP
    \s+(?P<path>\S+)                    # Ruta
    \s+HTTP/\d\.\d"                     # Protocolo
    \s+(?P<status>\d{3})                # Código de estado
    \s+(?P<bytes>\d+)                   # Bytes transferidos
    \s+"(?P<referer>[^"]*)"             # Referer
    \s+"(?P<user_agent>[^"]*)"          # User-Agent
''', re.VERBOSE)

def parse_http_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log HTTP con grupos nombrados y re.VERBOSE."""
    m = PATRON_HTTP.match(linea)
    if not m:
        return None
    return {
        "ip": m.group("ip"),
        "timestamp": m.group("timestamp"),
        "method": m.group("method"),
        "path": m.group("path"),
        "status": int(m.group("status")),
        "bytes": int(m.group("bytes")),
        "referer": m.group("referer"),
        "user_agent": m.group("user_agent"),
    }


PATRON_ERROR = re.compile(r'''
    ^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]   # Timestamp
    \s+(?P<level>ERROR|WARNING|INFO|DEBUG|CRITICAL)              # Nivel
    \s+(?P<module>[\w.]+)                                        # Módulo
    \s+-\s+(?P<error_type>\w+):\s+                              # Tipo de error
    (?P<message>.+)$                                             # Mensaje
''', re.VERBOSE)

def parse_error_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log de errores de aplicación."""
    m = PATRON_ERROR.match(linea)
    if not m:
        return None
    return {
        "timestamp": m.group("timestamp"),
        "level": m.group("level"),
        "module": m.group("module"),
        "error_type": m.group("error_type"),
        "message": m.group("message"),
    }


PATRON_AUTH = re.compile(r'''
    ^\[AUTH\]\s+                                             # Prefijo AUTH
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})   # Timestamp
    \s+\|\s+user=(?P<user>\S+)                              # Usuario
    \s+\|\s+action=(?P<action>\w+)                          # Acción
    \s+\|\s+status=(?P<status>\w+)                          # Estado
    \s+\|\s+ip=(?P<ip>[\d.]+)                              # IP
    \s+\|\s+(?P<extra_key>\w+)=(?P<extra_val>\S+)          # Campo extra
''', re.VERBOSE)

def parse_auth_log(linea: str) -> Optional[Dict]:
    """Parsea log de autenticación usando lookbehind para extraer valores."""
    m = PATRON_AUTH.match(linea)
    if not m:
        return None
    # Extrae campos extra con lookbehind
    extras = {}
    for campo in re.finditer(r'(?<=\|)\s*(\w+)=(\S+)', linea):
        clave, valor = campo.group(1), campo.group(2)
        if clave not in ('user', 'action', 'status', 'ip'):
            extras[clave] = valor
    return {
        "timestamp": m.group("timestamp"),
        "user": m.group("user"),
        "action": m.group("action"),
        "status": m.group("status"),
        "ip": m.group("ip"),
        "extra": extras,
    }


PATRON_DB_QUERY = re.compile(r'''
    ^\[DB-(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # Timestamp
    \s+QUERY\s+executed\s+in\s+(?P<time>[\d.]+)s:                 # Tiempo ejecución
    \s+(?P<query>.+)$                                              # Query
''', re.VERBOSE)

PATRON_DB_SLOW = re.compile(r'''
    ^\[DB-(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # Timestamp
    \s+SLOW_QUERY\s+\((?P<time>[\d.]+)s\):                        # Tiempo ejecución
    \s+(?P<query>.+)$                                              # Query
''', re.VERBOSE)

def parse_db_log(linea: str) -> Optional[Dict]:
    """Parsea log de base de datos, detectando QUERY y SLOW_QUERY."""
    m = PATRON_DB_SLOW.match(linea)
    if m:
        return {
            "timestamp": m.group("timestamp"),
            "query_type": "SLOW_QUERY",
            "execution_time": float(m.group("time")),
            "query": m.group("query"),
        }
    m = PATRON_DB_QUERY.match(linea)
    if m:
        return {
            "timestamp": m.group("timestamp"),
            "query_type": "QUERY",
            "execution_time": float(m.group("time")),
            "query": m.group("query"),
        }
    return None


# ══════════════════════════════════════════════════════════════════
#                PARTE 2: ANALIZADOR DE SEGURIDAD
# ══════════════════════════════════════════════════════════════════

def detectar_ataques_fuerza_bruta(logs_auth: List[Dict]) -> List[Dict]:
    """Detecta IPs con más de 3 intentos fallidos de login."""
    conteo = Counter()
    for log in logs_auth:
        if log.get("status") == "FAILED":
            conteo[log["ip"]] += 1
    return [{"ip": ip, "intentos": n} for ip, n in conteo.items() if n > 3]


PATRONES_SQL_INJECTION = [
    r"(?i)\bOR\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+",
    r"(?i)\bUNION\b.*\bSELECT\b",
    r"--",
    r"(?i)\bDROP\b\s+\bTABLE\b",
    r"(?i)\bDELETE\b\s+\bFROM\b.*\bWHERE\b\s+1\s*=\s*1",
]

def detectar_sql_injection(logs_db: List[Dict]) -> List[Dict]:
    """Detecta posibles intentos de SQL injection en queries."""
    sospechosos = []
    for log in logs_db:
        query = log.get("query", "")
        for patron in PATRONES_SQL_INJECTION:
            if re.search(patron, query, re.IGNORECASE):
                sospechosos.append({"query": query, "timestamp": log.get("timestamp")})
                break
    return sospechosos


PATRON_PATH_TRAVERSAL = re.compile(
    r'(?:\.\./|\.\.\\|%2e%2e%2f|%2e%2e/|\.\.%2f)',
    re.IGNORECASE
)

def detectar_path_traversal(logs_http: List[Dict]) -> List[Dict]:
    """Detecta intentos de path traversal en rutas HTTP."""
    return [
        {"path": log["path"], "ip": log["ip"], "timestamp": log["timestamp"]}
        for log in logs_http
        if PATRON_PATH_TRAVERSAL.search(log.get("path", ""))
    ]


def detectar_errores_criticos(logs_error: List[Dict]) -> List[Dict]:
    """Filtra errores de nivel ERROR o CRITICAL."""
    criticos = [
        log for log in logs_error
        if log.get("level") in ("ERROR", "CRITICAL")
    ]
    return sorted(criticos, key=lambda x: x.get("timestamp", ""))


# ══════════════════════════════════════════════════════════════════
#               PARTE 3: GENERADOR DE REPORTES
# ══════════════════════════════════════════════════════════════════

def clasificar_linea(linea: str) -> str:
    """Clasifica una línea de log por su tipo."""
    if re.match(r'^\d{1,3}(?:\.\d{1,3}){3}', linea):
        return 'http'
    if re.match(r'^\[20\d{2}-\d{2}-\d{2}', linea):
        return 'error'
    if re.match(r'^\[AUTH\]', linea):
        return 'auth'
    if re.match(r'^\[DB-', linea):
        return 'db'
    return 'desconocido'


def generar_reporte(logs: str) -> Dict:
    """Genera un reporte completo analizando todos los logs."""
    lineas = [l for l in logs.splitlines() if l.strip()]

    conteo_tipo = {"http": 0, "error": 0, "auth": 0, "db": 0, "desconocido": 0}
    logs_http, logs_error, logs_auth, logs_db = [], [], [], []

    for linea in lineas:
        tipo = clasificar_linea(linea)
        conteo_tipo[tipo] = conteo_tipo.get(tipo, 0) + 1
        if tipo == 'http':
            p = parse_http_log(linea)
            if p:
                logs_http.append(p)
        elif tipo == 'error':
            p = parse_error_log(linea)
            if p:
                logs_error.append(p)
        elif tipo == 'auth':
            p = parse_auth_log(linea)
            if p:
                logs_auth.append(p)
        elif tipo == 'db':
            p = parse_db_log(linea)
            if p:
                logs_db.append(p)

    # Estadísticas HTTP
    por_status = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
    rutas = Counter()
    ips = Counter()
    for log in logs_http:
        s = log["status"]
        if 200 <= s < 300:
            por_status["2xx"] += 1
        elif 300 <= s < 400:
            por_status["3xx"] += 1
        elif 400 <= s < 500:
            por_status["4xx"] += 1
        elif 500 <= s < 600:
            por_status["5xx"] += 1
        # Normaliza ruta (quita query string)
        ruta = re.sub(r'\?.*', '', log["path"])
        rutas[ruta] += 1
        ips[log["ip"]] += 1

    # Estadísticas de errores
    por_nivel = Counter(log["level"] for log in logs_error)
    por_modulo = Counter(log["module"] for log in logs_error)

    # Rendimiento DB
    tiempos = [log["execution_time"] for log in logs_db]
    queries_lentos = [log for log in logs_db if log["query_type"] == "SLOW_QUERY"]
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0

    return {
        "resumen": {
            "total_lineas": len(lineas),
            "por_tipo": {k: v for k, v in conteo_tipo.items() if k != "desconocido"},
        },
        "http": {
            "total_requests": len(logs_http),
            "por_status": por_status,
            "top_rutas": rutas.most_common(5),
            "top_ips": ips.most_common(5),
        },
        "errores": {
            "total": len(logs_error),
            "por_nivel": dict(por_nivel),
            "por_modulo": dict(por_modulo),
        },
        "seguridad": {
            "alertas_fuerza_bruta": detectar_ataques_fuerza_bruta(logs_auth),
            "alertas_sql_injection": detectar_sql_injection(logs_db),
            "alertas_path_traversal": detectar_path_traversal(logs_http),
        },
        "rendimiento": {
            "queries_lentos": queries_lentos,
            "tiempo_promedio_queries": tiempo_promedio,
        },
    }


# ══════════════════════════════════════════════════════════════════
#                VISUALIZACIÓN DEL REPORTE
# ══════════════════════════════════════════════════════════════════

def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte de forma legible."""
    print("=" * 70)
    print("                    REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 70)

    print("\n📊 RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de líneas procesadas: {reporte['resumen']['total_lineas']}")
    print("Por tipo:")
    for tipo, count in reporte['resumen']['por_tipo'].items():
        print(f"  • {tipo.upper()}: {count}")

    if 'http' in reporte:
        print("\n🌐 LOGS HTTP")
        print("-" * 40)
        print(f"Total requests: {reporte['http']['total_requests']}")
        print("Por código de estado:")
        for status, count in reporte['http']['por_status'].items():
            print(f"  • {status}: {count}")
        print("Top 5 rutas más solicitadas:")
        for ruta, count in reporte['http'].get('top_rutas', [])[:5]:
            print(f"  • {ruta}: {count} requests")

    if 'errores' in reporte:
        print("\n❌ ERRORES")
        print("-" * 40)
        print(f"Total errores: {reporte['errores']['total']}")
        print("Por nivel:")
        for nivel, count in reporte['errores']['por_nivel'].items():
            print(f"  • {nivel}: {count}")

    if 'seguridad' in reporte:
        print("\n🔒 ALERTAS DE SEGURIDAD")
        print("-" * 40)

        fb = reporte['seguridad'].get('alertas_fuerza_bruta', [])
        if fb:
            print(f"⚠️  Posibles ataques de fuerza bruta: {len(fb)}")
            for alerta in fb:
                print(f"     IP: {alerta['ip']} - {alerta['intentos']} intentos fallidos")

        sql = reporte['seguridad'].get('alertas_sql_injection', [])
        if sql:
            print(f"⚠️  Posibles SQL Injection: {len(sql)}")
            for alerta in sql[:3]:
                print(f"     Query: {alerta['query'][:60]}...")

        pt = reporte['seguridad'].get('alertas_path_traversal', [])
        if pt:
            print(f"⚠️  Posibles Path Traversal: {len(pt)}")
            for alerta in pt[:3]:
                print(f"     Ruta: {alerta['path']}")

    if 'rendimiento' in reporte:
        print("\n⏱️  RENDIMIENTO")
        print("-" * 40)
        print(f"Queries lentos detectados: {len(reporte['rendimiento'].get('queries_lentos', []))}")
        if 'tiempo_promedio_queries' in reporte['rendimiento']:
            print(f"Tiempo promedio de queries: {reporte['rendimiento']['tiempo_promedio_queries']:.3f}s")

    print("\n" + "=" * 70)


# ══════════════════════════════════════════════════════════════════
#                  BONUS: FUNCIONALIDADES EXTRA
# ══════════════════════════════════════════════════════════════════

import json

def exportar_reporte_json(reporte: Dict, archivo: str) -> None:
    """Exporta el reporte a un archivo JSON."""
    reporte_serializable = json.loads(json.dumps(reporte, default=str))
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(reporte_serializable, f, indent=2, ensure_ascii=False)
    print(f"✅ Reporte exportado a: {archivo}")


def analisis_temporal(logs_http: List[Dict]) -> Dict:
    """Analiza distribución de requests por hora."""
    conteo = Counter()
    for log in logs_http:
        m = re.search(r':(\d{2}):', log.get("timestamp", ""))
        if m:
            hora = int(m.group(1))
            conteo[hora] += 1
    return dict(sorted(conteo.items()))


def detectar_bots(logs_http: List[Dict]) -> List[Dict]:
    """Detecta requests que parecen venir de bots conocidos."""
    patron_bots = re.compile(
        r'(?i)(curl|wget|python-requests|scrapy|sqlmap|nikto|nmap|masscan|bot|spider|crawler)',
    )
    return [
        log for log in logs_http
        if patron_bots.search(log.get("user_agent", ""))
    ]


# ══════════════════════════════════════════════════════════════════
#                           MAIN
# ══════════════════════════════════════════════════════════════════

LOGS_PRUEBA = """
192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0 (Windows NT 10.0)"
192.168.1.101 - - [15/Mar/2024:10:23:46 -0600] "POST /api/login HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.102 - - [15/Mar/2024:10:23:47 -0600] "GET /admin/../../../etc/passwd HTTP/1.1" 403 0 "-" "sqlmap/1.0"
[2024-03-15 10:24:00] INFO app.startup - ApplicationStarted: Application started successfully on port 8080
[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused to host db.server.com:5432
[2024-03-15 10:25:15] WARNING app.cache - CacheWarning: Redis connection timeout, using fallback
[2024-03-15 10:26:00] ERROR app.auth - AuthenticationError: Invalid token for user admin@empresa.com
[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
[AUTH] 2024-03-15 10:31:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=1
[AUTH] 2024-03-15 10:31:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=2
[AUTH] 2024-03-15 10:32:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=3
[AUTH] 2024-03-15 10:32:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=4
[AUTH] 2024-03-15 10:33:00 | user=otro@empresa.com | action=LOGOUT | status=SUCCESS | ip=10.0.0.10 | session=def456uvw
[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users WHERE email = 'admin@empresa.com'
[DB-2024-03-15 10:35:25] QUERY executed in 0.012s: SELECT id, name FROM products WHERE active = 1
[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders o JOIN products p ON o.product_id = p.id JOIN users u ON o.user_id = u.id
[DB-2024-03-15 10:37:00] QUERY executed in 0.001s: SELECT * FROM users WHERE username = 'admin' OR 1=1--'
[DB-2024-03-15 10:38:00] QUERY executed in 0.002s: SELECT * FROM users UNION SELECT * FROM passwords
192.168.1.200 - - [15/Mar/2024:10:40:00 -0600] "GET /products?id=1 HTTP/1.1" 200 5678 "https://tienda.com" "Mozilla/5.0"
192.168.1.200 - - [15/Mar/2024:10:40:05 -0600] "GET /products?id=2 HTTP/1.1" 200 4321 "https://tienda.com" "Mozilla/5.0"
192.168.1.201 - - [15/Mar/2024:10:41:00 -0600] "GET /api/users HTTP/1.1" 401 123 "-" "PostmanRuntime/7.26.8"
192.168.1.201 - - [15/Mar/2024:10:41:05 -0600] "GET /api/users HTTP/1.1" 500 0 "-" "PostmanRuntime/7.26.8"
[2024-03-15 10:42:00] ERROR app.api - NullPointerException: Cannot read property 'id' of undefined
[DB-2024-03-15 10:45:00] SLOW_QUERY (5.2s): SELECT COUNT(*) FROM logs WHERE date > '2024-01-01'
""".strip()


if __name__ == "__main__":
    # ── Prueba de parsers individuales ──────────────────────────────
    print("PRUEBA DE PARSERS")
    print("=" * 50)

    linea_http = '192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"'
    print("\n-- Parser HTTP --")
    print(f"Entrada: {linea_http[:60]}...")
    print(f"Resultado: {parse_http_log(linea_http)}")

    linea_error = "[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused"
    print("\n-- Parser Error --")
    print(f"Entrada: {linea_error}")
    print(f"Resultado: {parse_error_log(linea_error)}")

    linea_auth = "[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz"
    print("\n-- Parser Auth --")
    print(f"Entrada: {linea_auth}")
    print(f"Resultado: {parse_auth_log(linea_auth)}")

    linea_db = "[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users"
    print("\n-- Parser DB --")
    print(f"Entrada: {linea_db}")
    print(f"Resultado: {parse_db_log(linea_db)}")

    # ── Reporte completo ─────────────────────────────────────────────
    print("\nGENERANDO REPORTE COMPLETO...\n")
    reporte = generar_reporte(LOGS_PRUEBA)
    mostrar_reporte(reporte)

    # ── Bonus ────────────────────────────────────────────────────────
    exportar_reporte_json(reporte, "reporte.json")
