import matplotlib.pyplot as plt

BAR_COLOR = "#1d4ed8"

def _empty_figure():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, "Нет данных для отображения",
            ha="center", va="center", fontsize=14)
    ax.set_axis_off()
    return fig

def plot_top_items(top):
    if top.empty:
        return _empty_figure()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["item_name"], top["revenue"], color=BAR_COLOR)
    ax.invert_yaxis()
    ax.set_title(f"Топ-{len(top)} товаров по выручке")
    ax.set_xlabel("Выручка")
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=3)
    ax.margins(x=0.12)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    return fig

def plot_category_share(by_category):
    if by_category.empty:
        return _empty_figure()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(by_category["category"], by_category["share"], color=BAR_COLOR)
    ax.invert_yaxis()
    ax.set_title("Доля категорий в выручке")
    ax.set_xlabel("Доля в выручке среза, %")
    ax.bar_label(ax.containers[0], fmt="%.1f%%", padding=3)
    ax.margins(x=0.12)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    return fig

def plot_orders_by_weekday(by_day):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(by_day["weekday"], by_day["orders"], color=BAR_COLOR)
    ax.set_title("Количество заказов по дням недели")
    ax.set_ylabel("Заказы")
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=3)
    ax.margins(y=0.15)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig