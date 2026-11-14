# Uplift Criteo

Учебный проект: uplift-моделирование на датасете Criteo Uplift Prediction (v2.1).

## Требования
- Python 3.11.x (у меня 3.11.7)
- Git
- VS Code (расширения Python, Jupyter)
- GitHub Desktop (по желанию) https://desktop.github.com

## Быстрый старт (для каждого участника)
1. `git clone <URL-репозитория>`     через git bash
2. `py --list` посмотрите список версий python, будем работать на 3.11.х (у меня 3.11.7)
https://www.python.org/downloads/windows/      адрес сайта
https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe         ссылка для скачивания
3. `py -3.11 -m venv .venv`         - явное указание нужной версии для .venv
4. `.venv\Scripts\activate` (Windows - для других ОС отличается)
5. `pip install -r requirements.txt`
6. `nbstripout --install`     настраивает Git так, чтобы выходные данные Jupyter-ноутбуков автоматически удалялись перед коммитом
7. Скачать датасет: см. `data/raw/README.md` (или просто запустить `python scripts/common/prepare_data.py` — он скачает сам)
8. Запустить `python scripts/common/prepare_data.py` (создаст `data/splits/*.npy`   , скачает датасет если его нет)
9. Get-FileHash data/raw/criteo-uplift.csv -Algorithm SHA256           Проверить контрольную сумму
   E4D7C710CA1F38E523309D0F8A0745D1B53E7392D51F20D1088B6CFEAEF222EF
10. Для трека С (с учетом CPU) pip install torch==2.13.0 --extra-index-url https://download.pytorch.org/whl/cpu
    Установить в случае необходимости (Для треков A, B - не требуется)

## Теория и задания
- `docs\criteo_uplift_theory_and_tasks.ipynb`

## Дополнительные команды
py --list     список версий py
py -3.11 -m venv --upgrade .venv        изменение версии .venv если поставили не ту (но лучше через deactivate, remove item ... ! )
ctrl shift X       расширения в VScode
pip install some-package        установка библиотеки какой то
pip show some-package           покажет название, и версию (если используете какую то новую библиотеку ОБЯЗАТЕЛЬНО добавить в req.txt)


## Структура
- `data/raw/` — сырой CSV (не в git). Ссылка и SHA256 в `data/raw/README.md`.
- `data/splits/` — train/val/test индексы (в git). Не пересобирать без согласования.
- `notebooks/<имя>/` — личные ноутбуки. Только в своей папке.
- `scripts/common/` — общий код (метрики, загрузка). Менять только по согласованию.
- `scripts/<имя>/` — личные скрипты.
- `outputs/<имя>/` — модели, графики (не в git).

## Правила работы
- В `main` напрямую не пушим. Только через PR из своей ветки.
- Перед созданием ветки: `git checkout main && git pull`.
- Ветка называется `<имя>/кратко-задача`, например `vlad/uplift-baseline`.
- Работаем только в своих папках `notebooks/<имя>/` и `scripts/<имя>/`.

## Что коммитится, а что нет
- **В git:** код (`scripts/`), ноутбуки (`notebooks/`), `data/splits/*.npy`, `requirements.txt`, `README.md`, финальные отчёты (`reports/`).
- **Не в git:** `data/raw/`, `data/processed/`, `outputs/`, `.venv/`, все `*.pkl`, `*.parquet`, `*.zip`, `*.gz`, а также `*.png` и `*.csv` **вне** `reports/`.

Если сомневаетесь, должен ли файл быть в git, — спросите руководителя (или нейронку) перед `git add`.

## Участники и зоны ответственности
- Vlad (руководитель): общая инфраструктура, `scripts/common/`, ревью. Трек C
- Egor: Трек B
- Andrew: Трек A

## Структура репозитория

uplift-criteo/
├── .gitignore                 # В GIT.  Обязателен с первого дня.
├── README.md                  # В GIT.  Инструкция для команды + описание проекта.
├── requirements.txt           # В GIT.  Точные версии всех библиотек.
│
├── data/
│   ├── raw/                   # НЕ в git.  Датасет Criteo (~3.55 ГБ) лежит локально.
│   │   └── README.md          # В GIT.   Ссылка + SHA256 датасета (чтобы все скачали одинаковый).
│   ├── processed/             # НЕ в git.  Промежуточные файлы (parquet после препроцессинга).
│   └── splits/                # В GIT.   train_idx.npy, val_idx.npy, test_idx.npy. Маленькие, фиксируют разбиение.
│
├── docs/                      # В GIT.  Общие материалы для всех (не личные).
│   └── criteo_uplift_theory_and_tasks.ipynb  # Теория и задания. Не редактируем, только читаем; если нужны заметки — в своей папке
│
├── notebooks/
│   ├── vlad/                  # Только ноутбуки Vlad.
│   ├── egor/                  # Только ноутбуки Egor.
│   └── andrew/                # Только ноутбуки Andrew.
│
├── scripts/
│   ├── common/                # В GIT.  Общий код. Меняется по согласованию.
│   │   ├── __init__.py        # Пустой, нужен чтобы работал `from scripts.common import ...`.
│   │   ├── data.py            # Загрузка Criteo, единый препроцессинг.
│   │   ├── metrics.py         # Qini, AUUC, uplift@k. Одна реализация на всех.
│   │   └── prepare_data.py    # Собирает data/splits/*.npy. Запускает только руководитель.
│   ├── vlad/                  # Только скрипты Vlad.
│   ├── egor/                  # Только скрипты Egor.
│   └── andrew/                # Только скрипты Andrew.
│
├── outputs/                   # НЕ в git.  Модели (.pkl), графики (.png), метрики (.csv).
│   ├── vlad/                  # Только артефакты Vlad.
│   ├── egor/                  # Только артефакты Egor.
│   └── andrew/                # Только артефакты Andrew.
│
└── reports/                   # В GIT.  Только финальные материалы для сдачи.
    └── figures/               # Итоговые Qini-кривые, сравнительные графики.