import pandas as pd
import os

def merge_files(base_path, titles_path, output_path):
    print(f"Loading Base File: {base_path}")
    try:
        df_base = pd.read_excel(base_path)
    except Exception as e:
        print(f"Error loading base file: {e}")
        return

    print(f"Loading Titles File: {titles_path}")
    try:
        df_titles = pd.read_excel(titles_path)
    except Exception as e:
        print(f"Error loading titles file: {e}")
        return

    print(f"Rows in Base: {len(df_base)}")
    print(f"Rows in Titles: {len(df_titles)}")

    # Clean and Standardize 'Causa' columns
    print("Normalizing 'Causa' columns...")
    
    # Base File: GUEVEL TF 2025 (22-12-2025).xlsx (Has 'Causa') - MANTENER TODAS LAS FILAS
    if 'Causa' in df_base.columns:
        df_base['Join_Key'] = pd.to_numeric(df_base['Causa'], errors='coerce')
        invalid_base = df_base['Join_Key'].isna().sum()
        if invalid_base > 0:
            print(f"Warning: {invalid_base} rows in Base have invalid/missing Causa (will be kept but won't match)")
        df_base['Join_Key'] = df_base['Join_Key'].apply(
            lambda x: str(int(x)).strip() if pd.notna(x) else None
        )
    else:
        print("ERROR: 'Causa' column not found in Base file!")
        return

    # Titles File: Pedir titulos TF 25-06-2025 Parte 1 pedidos.xlsx (Has 'CAUSA')
    if 'CAUSA' in df_titles.columns:
        df_titles['Join_Key'] = pd.to_numeric(df_titles['CAUSA'], errors='coerce')
        invalid_titles = df_titles['Join_Key'].isna().sum()
        if invalid_titles > 0:
            print(f"Dropped {invalid_titles} rows from Titles due to invalid/missing CAUSA")
            df_titles = df_titles.dropna(subset=['Join_Key'])
        df_titles['Join_Key'] = df_titles['Join_Key'].astype(int).astype(str).str.strip()
    else:
        print("ERROR: 'CAUSA' column not found in Titles file!")
        return

    # Perform Left Join to keep all records from Base file (GUEVEL TF 2025)
    print("Merging files (Left Join by Causa - keeping all GUEVEL rows)...")
    merged_df = pd.merge(
        df_base, 
        df_titles, 
        on='Join_Key',
        how='left',
        suffixes=('_guevel', '_pedidos')
    )

    # Clean up: Drop the temporary join key
    merged_df = merged_df.drop(columns=['Join_Key'])

    print(f"Rows in Merged Result: {len(merged_df)}")
    
    # Check for non-matches (where Titles columns are null)
    if 'JUD ID' in merged_df.columns:
         non_matches = merged_df['JUD ID'].isna().sum()
         print(f"Rows from Base (GUEVEL) without a match in Titles (Pedidos): {non_matches}")
    
    matches = len(merged_df) - non_matches if 'JUD ID' in merged_df.columns else 0
    print(f"Rows with successful match: {matches}")

    merged_df.to_excel(output_path, index=False)
    print(f"Success! Merged file saved to: {output_path}")

if __name__ == "__main__":
    # Paths configuration
    # Base File (mantener todas las filas): GUEVEL TF 2025 (22-12-2025).xlsx
    base_file_path = "/home/peluche/Escritorio/Ramiro Bot/guevel-bot/GUEVEL TF 2025 (22-12-2025).xlsx"
    
    # Titles File (agregar datos): Pedir titulos TF 25-06-2025 Parte 1 pedidos.xlsx
    titles_file_path = "/home/peluche/Escritorio/Ramiro Bot/guevel-bot/Pedir titulos TF 25-06-2025 Parte 1 pedidos.xlsx"
    
    output_file_path = "/home/peluche/Escritorio/Ramiro Bot/guevel-bot/convert_title_to_excel/Guevel_Merge_Final.xlsx"

    merge_files(base_file_path, titles_file_path, output_file_path)
