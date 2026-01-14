import pandas as pd

def merge_excels():
    # Ajusta estos nombres a los reales
    archivo_falta = "Reporte Iniciadas 2023.xlsx"   # el principal
    archivo_planillas = "output.xlsx"  
    archivo_salida = "resultado_merged.xlsx"

    # 1. Leemos ambos DataFrame
    df_falta = pd.read_excel(archivo_falta)
    df_planillas = pd.read_excel(archivo_planillas)

    # 2. Merge (left join):
    #    - "df_falta" es el DataFrame principal (queremos conservar todas sus filas).
    #    - left_on="EXPEDIENTE" es la columna que en "falta" contiene el expediente.
    #    - right_on="N° Expediente" es la columna en "planillas" donde matchea.
    #    Ajusta estos nombres de columna a los que realmente tengas.
    df_merged = df_falta.merge(
        df_planillas,
        how="left",
        left_on="expedienteSAC",
        right_on="N° Expediente"
    )

    # 3. Opcional: Elegir y reordenar las columnas finales
    #    Asumamos que en df_falta tienes Repartición, Orden, Año, CARATULA, etc.
    #    y de df_planillas te interesan Planilla/PDF, Tasa, etc.
    #    Ajusta a tus verdaderos encabezados.
    columnas_finales = [
        "Repartición", 
        "Orden",
        "Año",
        "expedienteSAC",
        "CARATULA",
        "Planilla/PDF"
    ]
    # Conservamos solo las columnas que realmente existen
    df_merged = df_merged[[col for col in columnas_finales if col in df_merged.columns]]

    # 4. Exportar a un nuevo Excel
    df_merged.to_excel(archivo_salida, index=False)
    print(f"Merge completado. Guardado en: {archivo_salida}")

if __name__ == "__main__":
    merge_excels()
