import requests
import json
import pandas as pd
import sys
from config import cookies

def obtener_presentaciones():
    url = "https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/PresentacionSorteadasLista.aspx/MisPresentaciones"
    headers = {
        "Origin": "https://www.justiciacordoba.gob.ar",
        "Referer": "https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/PresentacionSorteadasLista.aspx",
        "Content-Type": "application/json",
        "Cookie": cookies,
    }
    data = {"pageSize": 99999, "pageIndex": 0}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json())
        return response.json()["d"]["ReturnData"]
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        return []


def machear_con_presentaciones(df, presentaciones):
    df["IdReference"] = ""

    for index, row in df.iterrows():
        presentacion = row.get("Presentación")
        if pd.notna(presentacion):
            matched = next(
                (p for p in presentaciones if p["Id"] == int(presentacion)), None
            )
            if matched:
                df.at[index, "IdReference"] = matched["IdReference"]
            else:
                df.at[index, "IdReference"] = "Not found"
        else:
            df.at[index, "IdReference"] = "Not found"

    return df


def main():
    if len(sys.argv) < 3:
        print("Uso: python get_id_references_custom.py <archivo_entrada> <archivo_salida>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    df = pd.read_excel(input_file)
    presentaciones = obtener_presentaciones()
    df_macheada = machear_con_presentaciones(df, presentaciones)
    df_macheada.to_excel(output_file, index=False)
    print(f"Archivo con IdReference creado exitosamente: {output_file}")


if __name__ == "__main__":
    main()
