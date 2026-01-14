import pandas as pd


def merge_reparticion():
    # 1. Nombres de archivo (ajusta si están en otra carpeta)
    archivo1 = "resultado_merged.xlsx"  # Encabezados: Repartición, Orden, Año, ...
    archivo2 = "titles.xlsx"  # Encabezados: Archivo, Nombre o Razón Social, CUIT, Repartición, Orden, Año, ...
    archivo_salida = "Presenta título y aporte 2023 (parte 1).xlsx"

    # 2. Leer ambos Excel
    df1 = pd.read_excel(archivo1)
    df2 = pd.read_excel(archivo2)

    # 3. Diccionario de equivalencias para unificar reparticiones
    map_reparticion = {
        "INM": "Inmueble",
        "AUT": "Automotor",
        "CI": "Comercio e Industria",
    }

    # 4. Normalizar la Repartición en df1 a “Inmueble”, “Automotor” o “Comercio e Industria”
    df1["Reparticion_norm"] = df1["Repartición"].replace(map_reparticion)

    # 5. Merge basándonos en (Orden, Año, Reparticion_norm) vs. (Orden, Año, Repartición) en df2
    df_merged = df1.merge(
        df2,
        how="left",
        left_on=["Orden", "Año", "Reparticion_norm"],
        right_on=["Orden", "Año", "Repartición"],
    )

    # 6. Quedarnos con columnas relevantes (ajusta según necesites)
    columnas_finales = [
        "Reparticion_norm",  # la vamos a renombrar luego
        "Orden",
        "Año",
        "expedienteSAC",
        "CARATULA",
        "Planilla/PDF",
        "Archivo",
        "Nombre o Razón Social",
        "CUIT",
        "Identificador",
        "Domicilio",
        "Matrícula",
        "Monto total",
        "Tipo de Persona",
    ]
    # Conservar solo columnas existentes
    columnas_finales = [c for c in columnas_finales if c in df_merged.columns]
    df_merged = df_merged[columnas_finales]

    # 7. Renombrar la columna "Reparticion_norm" a "Repartición"
    df_merged.rename(columns={"Reparticion_norm": "Repartición"}, inplace=True)
    df_merged.rename(columns={"expedienteSAC": "IdSAC"}, inplace=True)

    # 8. Guardar con formato básico (encabezado en negrita, ajuste ancho de columnas)
    #    utilizando XlsxWriter:
    with pd.ExcelWriter(archivo_salida, engine="xlsxwriter") as writer:
        df_merged.to_excel(writer, sheet_name="Sheet1", index=False)

        # Obtener workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Crear formato de encabezado en negrita
        header_format = workbook.add_format(
            {"bold": True, "text_wrap": True, "valign": "middle", "border": 1}
        )

        # Aplicar el formato a la fila de encabezados
        for col_num, value in enumerate(df_merged.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Ajustar ancho de columnas automáticamente
        for i, col in enumerate(df_merged.columns):
            # Calcular la anchura como el máximo entre la longitud del encabezado y la de los datos
            max_length = max(df_merged[col].astype(str).map(len).max(), len(col))
            worksheet.set_column(i, i, max_length + 2)

    print(f"Merge completado. Archivo generado: {archivo_salida}")


if __name__ == "__main__":
    merge_reparticion()
