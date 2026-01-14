import pandas as pd

df = pd.read_excel('Guevel_Merge_Final.xlsx')

print('=== VERIFICACIÓN DEL MERGE GUEVEL ===\n')
print(f'Total filas: {len(df)}')
print(f'Columnas: {len(df.columns)}')

# Verificar matches
matched = df[df['JUD ID'].notna()]
unmatched = df[df['JUD ID'].isna()]

print(f'\nFilas con match (encontradas en Pedir titulos TF): {len(matched)}')
print(f'Filas sin match: {len(unmatched)}')

print('\n=== COLUMNAS DEL ARCHIVO MERGED ===')
print('De GUEVEL TF 2025:', ['Archivo', 'Nombre', 'CUIT_guevel', 'Monto', 'Domicilio', 'Causa'])
print('De Pedir titulos TF:', ['JUD ID', 'CARATULA', 'CAUSA', 'CUIT_pedidos', 'PROCURADOR', 'ORDEN/AÑO'])

print('\n=== MUESTRA DE DATOS ===')
print('\nFilas CON match (primeras 5):')
print(matched[['Archivo', 'Causa', 'CAUSA', 'JUD ID', 'CARATULA', 'PROCURADOR']].head(5))

print('\nFilas SIN match (primeras 5):')
if len(unmatched) > 0:
    print(unmatched[['Archivo', 'Nombre', 'Causa', 'CUIT_guevel', 'Monto']].head(5))
else:
    print('No hay filas sin match')
