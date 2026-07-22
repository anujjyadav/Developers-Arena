"""
dashboard.py
============
Interactive Sales Dashboard - Data Analysis & Static Visualization Engine

This script:
  1. Loads and cleans the sales dataset
  2. Engineers derived features (rolling averages, customer value tiers, month buckets)
  3. Produces a suite of Seaborn statistical plots (line, bar, box, violin, heatmap,
     count) saved to the `visualizations/` folder
  4. Produces a combined 2x2 "static dashboard" figure with a coordinated color theme
  5. Builds the interactive Plotly dashboard (dropdowns, hover, animation) and
     writes it out as `visualizations/interactive_dashboard.html`

Run with:  python dashboard.py
"""

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# 0. CONFIG - cohesive color palette used across every chart (static + interactive)
# ---------------------------------------------------------------------------
PALETTE = {
    "Phone": "#4C6EF5",
    "Headphones": "#F76707",
    "Laptop": "#12B886",
    "Tablet": "#BE4BDB",
    "Monitor": "#FCC419",
}
REGION_PALETTE = {
    "East": "#4C6EF5",
    "North": "#12B886",
    "South": "#F76707",
    "West": "#BE4BDB",
}
BG = "#FAFAFA"
GRID = "#E0E0E0"
ACCENT = "#343A40"

sns.set_theme(style="whitegrid", rc={
    "axes.facecolor": BG,
    "figure.facecolor": "white",
    "grid.color": GRID,
    "axes.edgecolor": ACCENT,
    "text.color": ACCENT,
    "axes.labelcolor": ACCENT,
    "xtick.color": ACCENT,
    "ytick.color": ACCENT,
})

OUT_DIR = "visualizations"
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. LOAD + CLEAN DATA
# ---------------------------------------------------------------------------
def load_data(path="sales_data.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Sanity check: Total_Sales should equal Quantity * Price. Recompute if not.
    expected = df["Quantity"] * df["Price"]
    mismatch = (df["Total_Sales"] != expected).sum()
    if mismatch:
        print(f"[data check] {mismatch} rows had Total_Sales != Quantity*Price, recalculating.")
        df["Total_Sales"] = expected

    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Date"].dt.day_name()
    return df


def engineer_features(df):
    df = df.copy()
    # 7-day rolling average of daily total sales (as a trend smoother)
    daily = df.groupby("Date", as_index=False)["Total_Sales"].sum()
    daily["Rolling_7D"] = daily["Total_Sales"].rolling(7, min_periods=1).mean()
    df = df.merge(daily[["Date", "Rolling_7D"]], on="Date", how="left")

    # Customer value tier (segmentation) - each Customer_ID appears once in this
    # dataset, so segmentation is based on spend quartile per transaction.
    df["Value_Tier"] = pd.qcut(
        df["Total_Sales"], q=4, labels=["Bronze", "Silver", "Gold", "Platinum"]
    )
    return df, daily


# ---------------------------------------------------------------------------
# 2. SEABORN STATIC PLOTS
# ---------------------------------------------------------------------------
def plot_sales_trend(df, daily):
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=daily, x="Date", y="Total_Sales", ax=ax,
                 color="#ADB5BD", linewidth=1.2, label="Daily Sales", alpha=0.8)
    sns.lineplot(data=daily, x="Date", y="Rolling_7D", ax=ax,
                 color="#4C6EF5", linewidth=2.5, label="7-Day Rolling Avg")
    ax.set_title("Daily Sales Trend (Jan – Apr 2024)", fontsize=14, weight="bold")
    ax.set_ylabel("Total Sales ($)")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/01_sales_trend_line.png", dpi=150)
    plt.close(fig)


def plot_product_bar(df):
    perf = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values(
        "Total_Sales", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=perf, x="Product", y="Total_Sales", hue="Product",
                palette=PALETTE, ax=ax, legend=False)
    for i, row in perf.reset_index(drop=True).iterrows():
        ax.text(i, row["Total_Sales"] + 3000, f"${row['Total_Sales']/1000:.0f}K",
                ha="center", fontsize=9, weight="bold", color=ACCENT)
    ax.set_title("Total Sales by Product", fontsize=14, weight="bold")
    ax.set_ylabel("Total Sales ($)")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/02_product_performance_bar.png", dpi=150)
    plt.close(fig)


def plot_price_box(df):
    """Box plot of unit price by product with a one-way ANOVA annotation."""
    fig, ax = plt.subplots(figsize=(8, 5))
    order = df.groupby("Product")["Price"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Product", y="Price", hue="Product", order=order,
                palette=PALETTE, ax=ax, legend=False)
    sns.stripplot(data=df, x="Product", y="Price", order=order,
                  color=ACCENT, alpha=0.35, size=3, ax=ax)

    groups = [df.loc[df["Product"] == p, "Price"].values for p in order]
    f_stat, p_val = stats.f_oneway(*groups)
    ax.text(0.02, 0.97, f"One-way ANOVA:  F = {f_stat:.2f},  p = {p_val:.3f}",
            transform=ax.transAxes, va="top", fontsize=9, style="italic",
            bbox=dict(boxstyle="round", facecolor="white", edgecolor=GRID))

    ax.set_title("Price Distribution by Product", fontsize=14, weight="bold")
    ax.set_ylabel("Unit Price ($)")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/03_price_distribution_box.png", dpi=150)
    plt.close(fig)


def plot_quantity_violin(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    order = ["North", "South", "East", "West"]
    sns.violinplot(data=df, x="Region", y="Quantity", hue="Region", order=order,
                   palette=REGION_PALETTE, ax=ax, inner="quartile", legend=False)
    means = df.groupby("Region")["Quantity"].mean().reindex(order)
    for i, m in enumerate(means):
        ax.scatter(i, m, color="white", edgecolor=ACCENT, zorder=5, s=40)
    ax.set_title("Quantity Sold Distribution by Region", fontsize=14, weight="bold")
    ax.set_ylabel("Units Sold per Order")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/04_quantity_violin.png", dpi=150)
    plt.close(fig)


def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    corr = df[["Quantity", "Price", "Total_Sales"]].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap=cmap, center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
                vmin=-1, vmax=1)
    ax.set_title("Correlation Matrix: Quantity, Price, Total Sales",
                 fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/05_correlation_heatmap.png", dpi=150)
    plt.close(fig)


def plot_value_tier_count(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    tier_order = ["Bronze", "Silver", "Gold", "Platinum"]
    tier_colors = ["#CD7F32", "#B0B0B0", "#D4AF37", "#7048E8"]
    sns.countplot(data=df, x="Region", hue="Value_Tier", hue_order=tier_order,
                  palette=tier_colors, ax=ax)
    ax.set_title("Customer Value Tier by Region", fontsize=14, weight="bold")
    ax.set_ylabel("Number of Orders")
    ax.set_xlabel("")
    ax.legend(title="Value Tier", frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/06_customer_segmentation_count.png", dpi=150)
    plt.close(fig)


def plot_combined_grid(df, daily):
    """2x2 subplot grid with a coordinated theme - the 'static dashboard'."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Sales Performance Overview", fontsize=17, weight="bold", y=1.02)

    # (0,0) trend
    ax = axes[0, 0]
    sns.lineplot(data=daily, x="Date", y="Rolling_7D", ax=ax, color="#4C6EF5", linewidth=2.5)
    ax.fill_between(daily["Date"], daily["Rolling_7D"], color="#4C6EF5", alpha=0.15)
    ax.set_title("7-Day Rolling Sales Trend", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))

    # (0,1) product bar
    ax = axes[0, 1]
    perf = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values(
        "Total_Sales", ascending=False)
    sns.barplot(data=perf, x="Product", y="Total_Sales", hue="Product",
                palette=PALETTE, ax=ax, legend=False)
    ax.set_title("Sales by Product", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))

    # (1,0) violin by region
    ax = axes[1, 0]
    sns.violinplot(data=df, x="Region", y="Quantity", hue="Region",
                   palette=REGION_PALETTE, ax=ax, inner="quartile", legend=False)
    ax.set_title("Quantity Sold by Region", weight="bold")
    ax.set_xlabel("")

    # (1,1) heatmap
    ax = axes[1, 1]
    corr = df[["Quantity", "Price", "Total_Sales"]].corr()
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap, center=0, square=True,
                linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax, vmin=-1, vmax=1)
    ax.set_title("Correlation Matrix", weight="bold")

    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/07_combined_dashboard_grid.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. PLOTLY INTERACTIVE DASHBOARD
# ---------------------------------------------------------------------------
def build_interactive_trend(df, daily):
    """Line chart with a Region dropdown filter + hover tooltips."""
    regions = ["All"] + sorted(df["Region"].unique().tolist())
    fig = go.Figure()

    # trace 0: "All" - overall rolling trend
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Rolling_7D"], mode="lines",
        name="All Regions", line=dict(color="#4C6EF5", width=3),
        hovertemplate="%{x|%b %d}<br>7D Avg: $%{y:,.0f}<extra></extra>",
        visible=True,
    ))

    region_daily = {}
    for region in regions[1:]:
        rd = df[df["Region"] == region].groupby("Date", as_index=False)["Total_Sales"].sum()
        rd["Rolling_7D"] = rd["Total_Sales"].rolling(7, min_periods=1).mean()
        region_daily[region] = rd
        fig.add_trace(go.Scatter(
            x=rd["Date"], y=rd["Rolling_7D"], mode="lines",
            name=region, line=dict(color=REGION_PALETTE[region], width=3),
            hovertemplate="%{x|%b %d}<br>7D Avg: $%{y:,.0f}<extra>" + region + "</extra>",
            visible=False,
        ))

    buttons = []
    n = len(fig.data)
    for i, region in enumerate(regions):
        vis = [False] * n
        vis[i] = True
        buttons.append(dict(label=region, method="update",
                             args=[{"visible": vis},
                                   {"title": f"Sales Trend — {region}"}]))

    fig.update_layout(
        title="Sales Trend (7-Day Rolling Average) — filter by Region",
        updatemenus=[dict(active=0, buttons=buttons, x=1.0, xanchor="right",
                           y=1.15, yanchor="top")],
        template="plotly_white", height=450,
        yaxis_title="Total Sales ($)", xaxis_title="",
        hovermode="x unified",
    )
    return fig


def build_interactive_segmentation(df):
    """Animated bubble chart: Price vs Quantity, animated by month, sized by
    Total_Sales, colored by Region -> a proxy for customer/segment behavior
    over time, with a dropdown to switch the color-grouping dimension."""
    d = df.copy()
    d["Month_dt"] = pd.to_datetime(d["Month"] + "-01")
    d = d.sort_values("Month_dt")

    fig = px.scatter(
        d, x="Quantity", y="Price", animation_frame="Month", animation_group="Customer_ID",
        size="Total_Sales", color="Region", color_discrete_map=REGION_PALETTE,
        hover_name="Customer_ID",
        hover_data={"Product": True, "Total_Sales": ":$,.0f", "Quantity": True,
                    "Price": ":$,.0f", "Region": False, "Month": False},
        size_max=45, range_x=[0, 10.5], range_y=[0, df["Price"].max() * 1.1],
        title="Customer Purchase Segmentation Over Time (bubble size = order value)",
    )
    fig.update_layout(template="plotly_white", height=520,
                       xaxis_title="Quantity Ordered", yaxis_title="Unit Price ($)",
                       legend_title="Region")
    return fig


def build_product_performance(df):
    """Grouped bar with dropdown to switch metric (Total Sales / Qty / Avg Price)."""
    metrics = {
        "Total Sales ($)": df.groupby("Product")["Total_Sales"].sum(),
        "Units Sold": df.groupby("Product")["Quantity"].sum(),
        "Avg Unit Price ($)": df.groupby("Product")["Price"].mean(),
    }
    products = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False).index.tolist()

    fig = go.Figure()
    for i, (label, series) in enumerate(metrics.items()):
        series = series.reindex(products)
        fig.add_trace(go.Bar(
            x=products, y=series.values,
            marker_color=[PALETTE[p] for p in products],
            name=label, visible=(i == 0),
            hovertemplate="%{x}<br>" + label + ": %{y:,.0f}<extra></extra>",
        ))

    buttons = []
    for i, label in enumerate(metrics):
        vis = [j == i for j in range(len(metrics))]
        buttons.append(dict(label=label, method="update",
                             args=[{"visible": vis}, {"yaxis": {"title": label}}]))

    fig.update_layout(
        title="Product Performance — choose a metric",
        updatemenus=[dict(active=0, buttons=buttons, x=1.0, xanchor="right", y=1.2)],
        template="plotly_white", height=450, showlegend=False,
        yaxis_title=list(metrics.keys())[0],
    )
    return fig


def build_correlation_heatmap_plotly(df):
    corr = df[["Quantity", "Price", "Total_Sales"]].corr().round(2)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                     zmin=-1, zmax=1, title="Correlation Matrix (interactive)")
    fig.update_layout(template="plotly_white", height=430)
    return fig


def build_full_dashboard_html(df, daily):
    """Stitch every interactive figure into one cohesive HTML dashboard page."""
    fig_trend = build_interactive_trend(df, daily)
    fig_perf = build_product_performance(df)
    fig_seg = build_interactive_segmentation(df)
    fig_corr = build_correlation_heatmap_plotly(df)

    html_parts = ["""
    <html><head><meta charset="utf-8">
    <title>Interactive Sales Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background:#FAFAFA; margin:0; padding:24px; color:#343A40;}
        h1 { text-align:center; }
        .subtitle { text-align:center; color:#868E96; margin-bottom:32px; }
        .card { background:white; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.06);
                padding:16px; margin-bottom:28px; }
        .grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
        @media (max-width:900px){ .grid{ grid-template-columns:1fr; } }
    </style></head><body>
    <h1>📊 Interactive Sales Dashboard</h1>
    <p class="subtitle">Sales Trends · Customer Segmentation · Product Performance (Jan – Apr 2024)</p>
    <div class="card">""",
        fig_trend.to_html(full_html=False, include_plotlyjs="cdn"),
        '</div><div class="grid">',
        '<div class="card">', fig_perf.to_html(full_html=False, include_plotlyjs=False), '</div>',
        '<div class="card">', fig_corr.to_html(full_html=False, include_plotlyjs=False), '</div>',
        '</div>',
        '<div class="card">', fig_seg.to_html(full_html=False, include_plotlyjs=False), '</div>',
        "</body></html>",
    ]

    with open(f"{OUT_DIR}/interactive_dashboard.html", "w") as f:
        f.write("\n".join(html_parts))

    return fig_trend, fig_perf, fig_seg, fig_corr


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------
def main():
    df = load_data("sales_data.csv")
    df, daily = engineer_features(df)

    print("Generating Seaborn static plots ...")
    plot_sales_trend(df, daily)
    plot_product_bar(df)
    plot_price_box(df)
    plot_quantity_violin(df)
    plot_correlation_heatmap(df)
    plot_value_tier_count(df)
    plot_combined_grid(df, daily)

    print("Generating Plotly interactive dashboard ...")
    build_full_dashboard_html(df, daily)

    print(f"Done. All outputs saved to ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
