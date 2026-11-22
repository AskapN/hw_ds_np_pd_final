import pandas as pd

def merge_data(orders, items, users):
    merged = orders.merge(users, on='user_id', how='left')
    merged = merged.merge(items, on='item_id', how='left')
    print(f"Объединено: {len(merged)} записей")
    return merged

def clean_data(merged_data):
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

    return df
