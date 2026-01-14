import argparse
import math
from pathlib import Path

import pandas as pd


def save_rows_in_range(input_file, output_file, start_row, end_row):
    data = pd.read_excel(input_file)

    if start_row < 0 or end_row > len(data):
        print("Rango fuera de los límites.")
        return

    filtered_data = data.iloc[start_row:end_row]
    filtered_data.to_excel(output_file, index=False)
    print(f"Archivo guardado con éxito en: {output_file}")


def _suffixes(n: int) -> list[str]:
    # A, B, C... (hasta 26)
    if n < 1 or n > 26:
        raise ValueError("chunks debe estar entre 1 y 26")
    return [chr(ord("A") + i) for i in range(n)]


def split_excel_in_chunks(input_file: Path, out_dir: Path, chunks: int) -> list[Path]:
    df = pd.read_excel(input_file)
    if df.empty:
        print("El archivo Excel está vacío.")
        return []

    out_dir.mkdir(parents=True, exist_ok=True)

    total_rows = len(df)
    chunk_size = int(math.ceil(total_rows / chunks))
    created: list[Path] = []

    for i, suffix in enumerate(_suffixes(chunks)):
        start = i * chunk_size
        end = min(start + chunk_size, total_rows)
        if start >= total_rows:
            break

        out_path = out_dir / f"{input_file.stem}_{suffix}{input_file.suffix}"
        df.iloc[start:end].to_excel(out_path, index=False)
        created.append(out_path)
        print(f"Creado: {out_path} (filas {start}..{end-1})")

    return created


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Nombre o ruta del Excel a partir del cual crear los chunks",
    )
    parser.add_argument(
        "--out-dir",
        "--output-dir",
        dest="out_dir",
        default=str(Path(__file__).resolve().parent / "tables"),
    )
    parser.add_argument(
        "--chunks",
        type=int,
        default=None,
        help="Cantidad de archivos a generar (A, B, C...).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Cantidad de filas por archivo (alternativa a --chunks).",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.is_absolute():
        # si te pasan solo el nombre, asumimos tables/
        tables_dir = Path(__file__).resolve().parent / "tables"
        candidate = tables_dir / input_path
        input_path = candidate if candidate.exists() else input_path

    if not input_path.exists():
        print(f"No existe: {input_path}")
        return 2

    if args.chunks is None and args.chunk_size is None:
        chunks = 4
        split_excel_in_chunks(input_path, Path(args.out_dir), chunks)
        return 0

    if args.chunks is not None and args.chunk_size is not None:
        print("Usá solo uno: --chunks o --chunk-size")
        return 2

    if args.chunks is not None:
        split_excel_in_chunks(input_path, Path(args.out_dir), args.chunks)
        return 0

    # args.chunk_size is not None
    df = pd.read_excel(input_path)
    if df.empty:
        print("El archivo Excel está vacío.")
        return 0

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    total_rows = len(df)
    chunk_size = max(1, int(args.chunk_size))
    chunks = int(math.ceil(total_rows / chunk_size))
    split_excel_in_chunks(input_path, out_dir, chunks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
