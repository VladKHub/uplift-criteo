import gzip
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split

RAW_DIR = Path("data/raw")
RAW_GZ = RAW_DIR / "criteo-research-uplift-v2.1.csv.gz"
RAW_CSV = RAW_DIR / "criteo-uplift.csv"
SPLITS_DIR = Path("data/splits")
PROCESSED_DIR = Path("data/processed")

# Что то из них может не работать
# URL = "http://go.criteo.net/criteo-research-uplift-v2.1.csv.gz"
URL = "https://huggingface.co/datasets/criteo/criteo-uplift/resolve/main/criteo-research-uplift-v2.1.csv.gz"

RANDOM_STATE = 42

DTYPES = {f"f{i}": "float32" for i in range(12)}
DTYPES.update({"treatment": "int8", "conversion": "int8", "visit": "int8", "exposure": "int8"})


def download_with_progress(url: str, dest: Path):
    """Скачивает файл по HTTP с прогресс-баром в консоли."""
    if dest.exists():
        print(f"[skip] {dest} уже существует")
        return
    print(f"Скачивание {url} → {dest}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        print(f"\r  {downloaded/1e6:.1f} / {total/1e6:.1f} MB ({pct:.1f}%)", end="")
    print("\nСкачивание завершено.")


def gunzip(src: Path, dest: Path):
    """Распаковывает .gz в обычный файл."""
    if dest.exists():
        print(f"[skip] {dest} уже существует")
        return
    print(f"Распаковка {src} → {dest}")
    with gzip.open(src, "rb") as f_in, open(dest, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("Распаковка завершена.")


def make_splits(df: pd.DataFrame):
    """Стратифицированный split по treatment: 60% train, 20% val, 20% test."""
    idx = np.arange(len(df))
    y = df["treatment"].values

    idx_train, idx_tmp = train_test_split(
        idx, test_size=0.4, stratify=y, random_state=RANDOM_STATE
    )
    idx_val, idx_test = train_test_split(
        idx_tmp, test_size=0.5, stratify=y[idx_tmp], random_state=RANDOM_STATE
    )
    return idx_train, idx_val, idx_test


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Скачать и распаковать
    download_with_progress(URL, RAW_GZ)
    gunzip(RAW_GZ, RAW_CSV)

    # 2. Прочитать с правильными типами
    print("Чтение CSV...")
    df = pd.read_csv(RAW_CSV, dtype=DTYPES)
    print(f"Строк: {len(df):,}, колонок: {len(df.columns)}")

    # 3. Сделать сплиты и сохранить индексы
    idx_train, idx_val, idx_test = make_splits(df)
    np.save(SPLITS_DIR / "train_idx.npy", idx_train)
    np.save(SPLITS_DIR / "val_idx.npy", idx_val)
    np.save(SPLITS_DIR / "test_idx.npy", idx_test)
    print(f"Сплиты сохранены: train={len(idx_train):,}, val={len(idx_val):,}, test={len(idx_test):,}")

    # 4. (Опционально) сохранить parquet для быстрого чтения в ноутбуках
    parquet_path = PROCESSED_DIR / "criteo_processed.parquet"
    if not parquet_path.exists():
        print("Сохранение parquet...")
        df.to_parquet(parquet_path, index=False)
    print("Готово.")


if __name__ == "__main__":
    main()