import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/criteo-uplift.csv")
PROCESSED_PATH = Path("data/processed/criteo_processed.parquet")

# Явные типы: 12 float-признаков + 4 бинарных колонки
DTYPES = {f"f{i}": "float32" for i in range(12)}
DTYPES.update({
    "treatment": "int8",
    "conversion": "int8",
    "visit": "int8",
    "exposure": "int8",
})

def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Читает сырой CSV Criteo с экономией памяти."""
    if not path.exists():
        raise FileNotFoundError(
            f"Файл {path} не найден. Сначала запустите scripts/common/prepare_data.py"
        )
    return pd.read_csv(path, dtype=DTYPES)

def load_processed(path: Path = PROCESSED_PATH) -> pd.DataFrame:
    """Читает parquet, если он уже собран; иначе — сырой CSV."""
    if path.exists():
        return pd.read_parquet(path)
    return load_raw()