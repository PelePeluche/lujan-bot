import requests
import json
import pandas as pd
import os
import sys
from config import cookies

def obtener_id_sac(codigo_presentacion, headers):
    url = "https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/ExpedientesListaLectura.aspx/ObtenerExpedientes"
    data = {"codigoPresentacion": codigo_presentacion, "pageSize": 1, "pageIndex": 0}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            respuesta_json = response.json()
            print("Respuesta JSON:", respuesta_json)
            if respuesta_json.get("d") and respuesta_json["d"].get("IsSuccess"):
                return (
                    respuesta_json["d"]["ReturnData"][0].get("IdSAC", "Not found")
                    if respuesta_json["d"]["ReturnData"]
                    else "Not found"
                )
            else:
                print("Error en la respuesta o IsSuccess es False")
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
            print(f"Error procesando la respuesta JSON: {e}")
            return None
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Uso: python get_id_sac_custom.py <archivo_entrada> <archivo_salida>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if os.path.exists(output_file):
        print(f"Cargando desde el archivo de progreso {output_file}")
        data = pd.read_excel(output_file, engine="openpyxl")
    else:
        print(f"Cargando desde el archivo original {input_file}")
        data = pd.read_excel(input_file, engine="openpyxl")

    for index, row in data.iterrows():
        presentacion = row["Presentación"]

        if pd.isna(presentacion):
            print(f"Fila {index} no tiene 'Presentación', se omite.")
            continue

        id_reference = row["IdReference"]

        if pd.isna(id_reference):
            print(f"Fila {index} no tiene 'IdReference', se omite.")
            continue

        codigo_presentacion = str(id_reference)

        headers = {
            "Origin": "https://www.justiciacordoba.gob.ar",
            "Referer": f"https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/ExpedientesListaLectura.aspx?codPres={codigo_presentacion}",
            "Content-Type": "application/json",
            "Cookie": cookies,
        }

        try:
            print(
                f"Obteniendo IdSAC para la fila {index} con Presentación {codigo_presentacion}..."
            )
            id_sac = obtener_id_sac(codigo_presentacion, headers)

            if id_sac:
                print(f"IdSAC encontrado: {id_sac}")
                data.at[index, "IdSAC"] = id_sac
            else:
                print(f"No se encontró IdSAC para la fila {index}.")
                data.at[index, "IdSAC"] = "Not found"

            data.to_excel(output_file, index=False, engine="openpyxl")

        except Exception as e:
            print(
                f"Error en la fila {index}: {e}. Intentando continuar con la siguiente fila."
            )

    print("Proceso completado.")


if __name__ == "__main__":
    main()
