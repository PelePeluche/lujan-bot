# Lujan Bot - Automatización de Demandas Judiciales

Bot de automatización para la carga de demandas ejecutivas fiscales en el sistema de Justicia Córdoba.

## Estructura del Proyecto

```
lujan-bot/
├── crea_demanda_bot/          # Bot principal para crear demandas
│   ├── steps/                 # Pasos modulares del proceso
│   ├── tables/                # Archivos Excel con datos
│   ├── config.py.example      # Plantilla de configuración
│   ├── main.py                # Script principal
│   ├── main_A.py              # Procesa parte A del Excel
│   ├── main_B.py              # Procesa parte B del Excel
│   ├── main_C.py              # Procesa parte C del Excel
│   ├── main_D.py              # Procesa parte D del Excel
│   └── split_excel.py         # Divide Excel en partes
├── convert_title_to_excel/    # Conversión de PDFs a Excel
│   ├── convert_title_to_excel.py
│   └── split_pdf_by_pages.py  # Divide PDFs multipágina
└── titles/                    # Carpeta para títulos (ignorada en git)

```

## Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd lujan-bot
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install selenium pandas openpyxl webdriver-manager PyPDF2
```

4. **Configurar credenciales**
```bash
cp crea_demanda_bot/config.py.example crea_demanda_bot/config.py
# Editar config.py con tus credenciales
```

## Uso

### 1. Convertir PDFs de Títulos a Excel

Si tienes PDFs con múltiples páginas (un título por página):

```bash
# Dividir PDF en archivos individuales
python convert_title_to_excel/split_pdf_by_pages.py

# Extraer datos de los títulos a Excel
python convert_title_to_excel/convert_title_to_excel.py
```

### 2. Dividir Excel en Partes

Para procesar en paralelo o por lotes:

```bash
python crea_demanda_bot/split_excel.py
```

Esto creará 4 archivos: `_A.xlsx`, `_B.xlsx`, `_C.xlsx`, `_D.xlsx`

### 3. Ejecutar el Bot

Procesar una parte específica:

```bash
venv/bin/python crea_demanda_bot/main_A.py
venv/bin/python crea_demanda_bot/main_B.py
venv/bin/python crea_demanda_bot/main_C.py
venv/bin/python crea_demanda_bot/main_D.py
```

O procesar un archivo específico:

```bash
venv/bin/python crea_demanda_bot/main.py --excel "mi_archivo.xlsx"
```

## Características

- ✅ Automatización completa del proceso de carga de demandas
- ✅ Extracción automática de datos desde PDFs
- ✅ División de trabajo en múltiples partes para procesamiento paralelo
- ✅ Carga automática de títulos y documentos de designación
- ✅ Manejo de errores y reintentos
- ✅ Guardado incremental del progreso en Excel

## Estructura de Datos del Excel

El Excel debe contener las siguientes columnas:

- `Archivo`: Nombre del archivo PDF del título
- `Nombre o Razón Social`: Nombre del demandado
- `CUIT`: CUIT del demandado
- `Repartición`: Tipo de repartición (INM, AUT, CI, TA)
- `Orden`: Número de orden
- `Año`: Año del título
- `Identificador`: Identificador tributario
- `Domicilio`: Domicilio del demandado
- `Matrícula`: Matrícula (si aplica)
- `Monto total`: Monto de la deuda
- `Tipo de Persona`: Física o Jurídica
- `Presentación`: (Se completa automáticamente con el número de presentación)

## Archivos Requeridos

Coloca los siguientes archivos en sus respectivas carpetas:

- **Títulos individuales**: `titles/<nombre_carpeta>/`
- **Archivo de designación**: `carga demandas enero 2026/designacion.pdf`
- **Excel con datos**: `crea_demanda_bot/tables/`

## Notas Importantes

- El bot requiere Chrome instalado
- Las credenciales en `config.py` son sensibles - nunca las subas a git
- El proceso guarda el progreso automáticamente en el Excel
- Si una fila ya tiene número de presentación, se salta automáticamente

## Licencia

Uso interno
# lujan-bot
