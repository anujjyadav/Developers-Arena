"""
test_dashboard.py
==================
Lightweight validation suite for the Sales Dashboard project.
Run with: python test_dashboard.py

Covers:
  - Data integrity checks on sales_data.csv
  - Feature engineering correctness (rolling average, value tiers)
  - Output file existence checks after running dashboard.py
"""
import os
import sys
import pandas as pd
import numpy as np

PASS = "PASS"
FAIL = "FAIL"
results = []


def check(name, condition):
    status = PASS if condition else FAIL
    results.append((name, status))
    print(f"[{status}] {name}")
    return condition


def main():
    # ---- 1. Raw data integrity -------------------------------------------------
    df = pd.read_csv("sales_data.csv")
    check("File loads and has 100 rows", len(df) == 100)
    check("Has exactly 7 columns", df.shape[1] == 7)
    check("No missing values anywhere", df.isnull().sum().sum() == 0)
    check("No duplicate Customer_IDs", df["Customer_ID"].is_unique)

    expected_total = df["Quantity"] * df["Price"]
    check("Total_Sales == Quantity * Price for every row",
          (df["Total_Sales"] == expected_total).all())

    df["Date"] = pd.to_datetime(df["Date"])
    check("Date column parses cleanly to datetime", df["Date"].notna().all())
    check("Date range is Jan 1 - Apr 9, 2024",
          df["Date"].min() == pd.Timestamp("2024-01-01") and
          df["Date"].max() == pd.Timestamp("2024-04-09"))

    check("Exactly 5 product categories", df["Product"].nunique() == 5)
    check("Exactly 4 regions", df["Region"].nunique() == 4)
    check("Quantity values are all positive integers",
          (df["Quantity"] > 0).all() and df["Quantity"].dtype.kind in "iu")
    check("Price values are all positive",
          (df["Price"] > 0).all())

    # ---- 2. Feature engineering correctness ------------------------------------
    daily = df.groupby("Date", as_index=False)["Total_Sales"].sum()
    daily["Rolling_7D"] = daily["Total_Sales"].rolling(7, min_periods=1).mean()
    manual_first = daily["Total_Sales"].iloc[0]
    check("7-day rolling average, first value == first daily total",
          np.isclose(daily["Rolling_7D"].iloc[0], manual_first))
    manual_7th = daily["Total_Sales"].iloc[:7].mean()
    check("7-day rolling average, 7th value == mean of first 7 days",
          np.isclose(daily["Rolling_7D"].iloc[6], manual_7th))

    tiers = pd.qcut(df["Total_Sales"], q=4, labels=["Bronze", "Silver", "Gold", "Platinum"])
    check("Value-tier segmentation produces exactly 4 tiers", tiers.nunique() == 4)
    check("Value-tier groups are roughly balanced (25 +/- 2 each)",
          tiers.value_counts().between(23, 27).all())

    # ---- 3. Output artifacts exist after running dashboard.py ------------------
    expected_files = [
        "visualizations/01_sales_trend_line.png",
        "visualizations/02_product_performance_bar.png",
        "visualizations/03_price_distribution_box.png",
        "visualizations/04_quantity_violin.png",
        "visualizations/05_correlation_heatmap.png",
        "visualizations/06_customer_segmentation_count.png",
        "visualizations/07_combined_dashboard_grid.png",
        "visualizations/interactive_dashboard.html",
    ]
    for f in expected_files:
        check(f"Output file exists: {f}", os.path.exists(f) and os.path.getsize(f) > 0)

    # ---- Summary ----------------------------------------------------------------
    n_pass = sum(1 for _, s in results if s == PASS)
    n_total = len(results)
    print(f"\n{n_pass}/{n_total} checks passed.")
    if n_pass != n_total:
        sys.exit(1)


if __name__ == "__main__":
    main()
