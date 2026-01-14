import pandas as pd
from pathlib import Path

def split_excel_into_parts(input_excel_path, output_folder, num_parts=4):
    """
    Divide un archivo Excel en múltiples partes (A, B, C, D, etc.)
    
    Args:
        input_excel_path: Ruta al archivo Excel original
        output_folder: Carpeta donde se guardarán los archivos divididos
        num_parts: Número de partes en las que dividir (default: 4)
    """
    # Leer el Excel
    df = pd.read_excel(input_excel_path)
    total_rows = len(df)
    
    print(f"Total de filas en el Excel: {total_rows}")
    
    # Calcular cuántas filas por parte
    rows_per_part = total_rows // num_parts
    remainder = total_rows % num_parts
    
    print(f"Filas por parte (aproximado): {rows_per_part}")
    
    # Letras para nombrar las partes
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    # Obtener el nombre base del archivo
    input_path = Path(input_excel_path)
    base_name = input_path.stem  # Sin extensión
    
    start_idx = 0
    for i in range(num_parts):
        # Calcular el rango de filas para esta parte
        if i < remainder:
            end_idx = start_idx + rows_per_part + 1
        else:
            end_idx = start_idx + rows_per_part
        
        # Extraer las filas correspondientes
        df_part = df.iloc[start_idx:end_idx].copy()
        
        # Nombre del archivo de salida
        output_filename = f"{base_name}_{letters[i]}.xlsx"
        output_path = Path(output_folder) / output_filename
        
        # Guardar la parte
        df_part.to_excel(output_path, index=False)
        
        print(f"✓ Creado: {output_filename} ({len(df_part)} filas)")
        
        start_idx = end_idx
    
    print(f"\n¡Proceso completado! Se crearon {num_parts} archivos.")


if __name__ == "__main__":
    # Configuración
    input_excel = "/Users/admin/Documents/Ramiro Bots/lujan-bot/crea_demanda_bot/tables/lujan (13-01-2026).xlsx"
    output_folder = "/Users/admin/Documents/Ramiro Bots/lujan-bot/crea_demanda_bot/tables"
    
    split_excel_into_parts(input_excel, output_folder, num_parts=4)
