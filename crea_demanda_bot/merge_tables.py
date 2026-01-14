import pandas as pd
import sys

def merge_tables(input_files, output_file):
    """
    Mergea múltiples archivos Excel en uno solo.
    """
    dataframes = []
    
    for file in input_files:
        print(f"Leyendo {file}...")
        df = pd.read_excel(file, engine="openpyxl")
        print(f"  - {len(df)} filas encontradas")
        dataframes.append(df)
    
    # Concatenar todos los dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    print(f"\nTotal de filas después del merge: {len(merged_df)}")
    print(f"Guardando en {output_file}...")
    
    merged_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"¡Archivo mergeado exitosamente!")
    print(f"\nColumnas: {merged_df.columns.tolist()}")
    print(f"Shape final: {merged_df.shape}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python merge_tables.py <archivo_salida> <archivo1> <archivo2> [archivo3] ...")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    merge_tables(input_files, output_file)

if __name__ == "__main__":
    main()
