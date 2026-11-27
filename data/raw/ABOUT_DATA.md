# Датасет Criteo Uplift v2.1

## Что скачивается (скачивание должно выполниться автоматически при запуске scripts/common/prepare_data.py)
- **Ссылка:** http://go.criteo.net/criteo-research-uplift-v2.1.csv.gz
              https://huggingface.co/datasets/criteo/criteo-uplift/resolve/main/criteo-research-uplift-v2.1.csv.gz
- **Формат:** gzip-архив (~297 МБ), внутри — CSV (~3.55 ГБ).
- **Строк:** 13 979 592, **колонок:** 16.
- **Колонки:** `f0`–`f11` (float, анонимизированные признаки), `treatment` (0/1), `conversion` (0/1), `visit` (0/1), `exposure` (0/1).

## Как получить файл
1. Самый простой способ: запустить `python scripts/common/prepare_data.py` из корня проекта. Скрипт сам скачает архив, распакует его и положит CSV в `data/raw/criteo-uplift.csv`.
2. Если скачиваете вручную: скачайте архив по ссылке выше, распакуйте, переименуйте получившийся CSV в `criteo-uplift.csv` и положите в эту папку.

## Проверка целостности (обязательно)
После скачивания вычислите SHA256 файла `criteo-uplift.csv`:
```powershell
Get-FileHash data/raw/criteo-uplift.csv -Algorithm SHA256
```

Должны получить 
```powershell
 E4D7C710CA1F38E523309D0F8A0745D1B53E7392D51F20D1088B6CFEAEF222EF
```

data/processed/criteo_processed.parquet — этот файл создаётся автоматически скриптом prepare_data.py. Это тот же датасет, но сохранённый в формате Parquet. Parquet читается в 5–10 раз быстрее обычного CSV и занимает меньше места, поэтому ноутбуки загружают данные из него, а не из гигантского CSV.

data/splits/*.npy — три файла (train_idx.npy, val_idx.npy, test_idx.npy). В них лежат не сами данные, а только числовые индексы строк: какие строки из общего датасета идут в train, какие в val, какие в test. Они маленькие (несколько мегабайт), поэтому коммитятся в git. Благодаря им у всех участников одно и то же разбиение, и результаты моделей можно сравнивать.