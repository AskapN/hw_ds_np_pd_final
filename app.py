import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_data, DataLoadError
from src.data_cleaner import merge_data, clean_data
from src import analysis as an
from src import visualization as viz


@st.cache_data
def get_data():
    orders, items, users = load_data()
    merged = merge_data(orders, items, users)
    return clean_data(merged)

st.title("Дашборд продаж")

try:
    df = get_data()
except DataLoadError as e:
    st.error(f"Не удалось загрузить данные: {e}")
    st.stop()

with st.sidebar:
    st.header("Фильтры")
    categories = st.multiselect(
        "Категория товара",
        options=sorted(df["category"].unique())
    )
    data_range = st.date_input(
        "Период заказов",
        value=[],
        min_value=df["order_date"].min().date(),
        max_value=df["order_date"].max().date(),
    )

filtered = df
if categories:
    filtered = filtered[filtered["category"].isin(categories)]
if len(data_range) == 2:
    start, end = data_range
    filtered = filtered[(filtered["order_date"].dt.date >= start) & (filtered["order_date"].dt.date <= end)]

tab_raw, tab_kpi, tab_chars, tab_insights = st.tabs(
    ["Сырые данные", "Ключевые показатели", "Визуализация", "Аналитические выводы"]
)

with tab_raw:
    st.subheader("Заказы + пользователи + товары")
    st.caption(f"Показано {len(filtered)} из {len(df)} записей")
    st.dataframe(filtered, hide_index=True)

with tab_kpi:
    st.subheader("Ключевые показатели")
    m = an.compute_metrics(filtered)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Заказы", m["n_orders"])
    c2.metric("Выручка", f"{m['revenue']:.2f}")
    c3.metric("Пользователи", m["n_users"])
    c4.metric("Средний чек", f"{m['avg_check']:.2f}")

with tab_chars:
    st.subheader("Визуализация")

    fig = viz.plot_top_items(an.top_items(filtered))
    st.pyplot(fig)
    plt.close(fig)

    fig = viz.plot_category_share(an.revenue_by_category(filtered))
    st.pyplot(fig)
    plt.close(fig)

    fig = viz.plot_orders_by_weekday(an.orders_by_weekday(filtered))
    st.pyplot(fig)
    plt.close(fig)

with tab_insights:
    st.subheader("Аналитические выводы")
    for line in an.build_conclusions(filtered):
        st.markdown(f"- {line}")