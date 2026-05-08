from validador import procesar_lote, CODIGOS_PRUEBA

def mostrar_reporte(reporte):
    print("=" * 60)
    print("                 REPORTE DE VALIDACIÓN LOGÍSTICA")
    print("=" * 60)
    print(f"\nTotal procesados: {reporte['total']}")
    if reporte['total'] > 0:
        print(f"Válidos: {reporte['validos']} ({reporte['validos']/reporte['total']*100:.1f}%)")
        print(f"Inválidos: {reporte['invalidos']} ({reporte['invalidos']/reporte['total']*100:.1f}%)")
    
    print("\nDesglose por tipo:")
    print("-" * 40)
    for tipo, stats in reporte["por_tipo"].items():
        if stats["total"] > 0:
            tasa = (stats["validos"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {tipo.capitalize():<12}: {stats['validos']:>2}/{stats['total']:<2} ({tasa:.0f}% válidos)")
    print("=" * 60)

if __name__ == "__main__":
    reporte_final = procesar_lote(CODIGOS_PRUEBA)
    mostrar_reporte(reporte_final)