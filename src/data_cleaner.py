import pandas as pd

def merge_data(orders, items, users):
    """Объединяет заказы с пользователями и товарами в одну таблицу.

    Args:
        orders (DataFrame): таблица заказов.
        items (DataFrame): таблица товаров.
        users (DataFrame): таблица пользователей.

    Returns:
        DataFrame: объединённая таблица «заказ + пользователь + товар».
    """
    merged = orders.merge(users, on='user_id', how='left')
    merged = merged.merge(items, on='item_id', how='left')
    print(f"Объединено: {len(merged)} записей")
    return merged

def clean_data(merged_data):
    """Очищает объединённую таблицу: приводит типы, заполняет пропуски, считает выручку.

    Args:
        merged_data (DataFrame): объединённая таблица заказов, пользователей и товаров.

    Returns:
        DataFrame: очищенная таблица с добавленным столбцом revenue.
    """
    df = merged_data.copy()

    # Приводим типы данных
    df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors='coerce')

    # Пропуски в справочных полях заполняем заглушкой (пропусков нет)
    for col in [
        "category", "item_name", "city", "user_segment", "supplier", "user_name"
    ]:
        df[col] = df[col].fillna("Unknown")

    # Строки без даты заказа или без суммы непригодны для расчетов
    df = df.dropna(subset=["order_date", "quantity", "price_per_unit"])

    # Добавляем столбец с выручкой
    df["revenue"] = df["quantity"] * df["price_per_unit"]

    return df
