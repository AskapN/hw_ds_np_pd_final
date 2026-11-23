from pathlib import Path
import pandas as pd
from config import DATA_PATH


class DataLoadError(Exception):
    """Ошибка загрузки данных — ловим её в app.py и показываем в UI."""
    pass


def load_data():
    """Загружает три CSV-таблицы (orders, items, users) из data/raw.

    Returns:
        tuple: (orders, items, users) — три pandas DataFrame.

    Raises:
        DataLoadError: если папка с данными не найдена или файлы некорректны.
    """

    if not DATA_PATH.exists():
        raise DataLoadError(f"Папка с данными не найдена: {DATA_PATH}")

    if not DATA_PATH.is_dir():
        raise DataLoadError(f"Путь не является папкой: {DATA_PATH}")

    try:
        items = pd.read_csv(DATA_PATH / "items.csv")
        orders = pd.read_csv(DATA_PATH / "orders.csv")
        users = pd.read_csv(DATA_PATH / "users.csv")
    except pd.errors.EmptyDataError as e:
        raise DataLoadError(f"Один из CSV пуст: {e}") from e
    except pd.errors.ParserError as e:
        raise DataLoadError(f"Ошибка парсинга CSV: {e}") from e
    except OSError as e:
        raise DataLoadError(f"Ошибка доступа к файлу: {e}") from e

    return orders, items, users