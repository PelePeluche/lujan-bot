import os
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_by_pages(input_pdf_path, output_folder):
    """
    Divide un PDF en archivos individuales, uno por página.
    
    Args:
        input_pdf_path: Ruta al archivo PDF de entrada
        output_folder: Carpeta donde se guardarán los PDFs individuales
    """
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Obtener el nombre base del archivo sin extensión
    pdf_filename = os.path.basename(input_pdf_path)
    pdf_name = os.path.splitext(pdf_filename)[0]
    
    # Leer el PDF
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    print(f"Procesando '{pdf_filename}' con {total_pages} páginas...")
    
    # Crear un PDF por cada página
    for page_num in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        # Nombre del archivo de salida: nombreoriginal_pag1.pdf, nombreoriginal_pag2.pdf, etc.
        output_filename = f"{pdf_name}_pag{page_num + 1}.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        # Guardar el PDF individual
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"  ✓ Creado: {output_filename}")
    
    print(f"Completado: {total_pages} archivos creados en '{output_folder}'\n")


def process_folder(input_folder, output_folder):
    """
    Procesa todos los PDFs en una carpeta y sus subcarpetas.
    
    Args:
        input_folder: Carpeta con los PDFs originales
        output_folder: Carpeta donde se guardarán todos los PDFs divididos
    """
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_count = 0
    
    # Recorrer todos los archivos en la carpeta y subcarpetas
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_count += 1
                input_pdf_path = os.path.join(root, filename)
                
                try:
                    split_pdf_by_pages(input_pdf_path, output_folder)
                except Exception as e:
                    print(f"Error procesando '{filename}': {e}\n")
    
    if pdf_count == 0:
        print("No se encontraron archivos PDF en la carpeta especificada.")
    else:
        print(f"Proceso completado. Se procesaron {pdf_count} archivo(s) PDF.")


if __name__ == "__main__":
    # Configuración
    input_folder = "/Users/admin/Documents/Ramiro Bots/lujan-bot/carga demandas enero 2026/titulos/titulos"
    output_base_folder = "/Users/admin/Documents/Ramiro Bots/lujan-bot/carga demandas enero 2026/titulos/titulos_separados"
    
    print("=" * 60)
    print("SCRIPT DE DIVISIÓN DE PDFs POR PÁGINA")
    print("=" * 60)
    print(f"Carpeta de entrada: {input_folder}")
    print(f"Carpeta de salida: {output_base_folder}")
    print("=" * 60 + "\n")
    
    process_folder(input_folder, output_base_folder)
    
    print("\n" + "=" * 60)
    print("¡Proceso finalizado!")
    print("=" * 60)
