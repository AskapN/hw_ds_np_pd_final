import pandas as pd

WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

def compute_metrics(df):
    """Считает ключевые показатели продаж.

    Args:
        df (DataFrame): очищенная таблица с колонками order_id, user_id и revenue.

    Returns:
        dict: ключи n_orders, revenue, n_users, avg_check.
    """
    n_orders = int(df["order_id"].nunique())
    revenue = float(df["revenue"].sum())
    n_users = int(df["user_id"].nunique())
    avg_check = revenue / n_orders if n_orders else 0.0
    return {
        "n_orders": n_orders,
        "revenue": revenue,
        "n_users": n_users,
        "avg_check": avg_check
    }

def top_items(df, n=10):
    """Возвращает топ товаров по выручке.

    Args:
        df (DataFrame): таблица с колонками item_name и revenue.
        n (int): сколько товаров вернуть.

    Returns:
        DataFrame: топ n товаров по убыванию выручки.
    """
    return (
        df.groupby("item_name", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(n)
    )

def revenue_by_category(df):
    """Считает выручку и её долю по категориям товаров.

    Args:
        df (DataFrame): таблица с колонками category и revenue.

    Returns:
        DataFrame: колонки category, revenue и share (доля в %).
    """
    by_cat = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending= False)
    )
    by_cat["share"] = by_cat["revenue"] / by_cat["revenue"].sum() * 100
    return by_cat

def orders_by_weekday(df):
    """Считает количество заказов по дням недели.

    Args:
        df (DataFrame): таблица с колонкой order_date (datetime).

    Returns:
        DataFrame: колонки weekday (Пн–Вс) и orders.
    """
    counts = (
        df["order_date"].dt.day_of_week
        .value_counts()
        .reindex(range(7), fill_value=0)
    )
    return pd.DataFrame({"weekday": WEEKDAYS, "orders": counts.to_numpy()})

def build_conclusions(df):
    """Формулирует аналитические выводы по данным.

    Args:
        df (DataFrame): очищенная таблица.

    Returns:
        list: список строк с выводами для отображения в Streamlit.
    """
    if df.empty:
        return ["Нет данных для выбранных фильтров - измените категорию или период"]

    conclusion = []

    by_cat = revenue_by_category(df)
    leader_cat = by_cat.iloc[0]
    conclusion.append(
        f"Основная выручка приходится на категорию '{leader_cat['category']}' - "
        f"{leader_cat['share']:.1f}% выручки среза ({leader_cat['revenue']:,.2f})."
    )

    leader_item = top_items(df, n=1).iloc[0]
    conclusion.append(
        f"Лидер продаж по выручке - '{leader_item['item_name']}' ({leader_item['revenue']:,.2f})."
    )

    by_day = orders_by_weekday(df)
    peak = by_day["orders"].max()
    peak_days = by_day.loc[by_day["orders"] == peak, "weekday"].tolist()
    weekend = by_day.loc[by_day["weekday"].isin(["Сб", "Вс"]), "orders"].sum()
    total = by_day["orders"].sum()
    conclusion.append(
        f"Пик заказов: {', '.join(peak_days)} - максимум заказов в день: {peak}. "
        f"На выходные (Сб, Вс) приходится {weekend / total * 100:.1f}% заказов ({weekend} из {total})."
    )

    m = compute_metrics(df)
    conclusion.append(
        f"Средний чек - {m['avg_check']:,.2f}. Заказов: {m['n_orders']}. "
        f"Уникальных пользователей: {m['n_users']}."
    )
    return conclusion
