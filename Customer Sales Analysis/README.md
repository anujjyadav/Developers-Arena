# Sales Performance & Customer Analytics

Analysis of customer purchasing patterns, top-customer identification, and a sales performance dashboard built from `sales_data.csv` (100 transactions) and `customer_churn.csv` (500 customer records).

## Contents

| File | Description |
|---|---|
| `Sales_Performance_Analysis.ipynb` | Full Jupyter notebook: EDA, data prep, aggregations, merging, pivot tables, and visualizations (pre-executed with outputs). |
| `Sales_Performance_Report.docx` | Executive report with embedded charts, tables, and business recommendations. |
| `requirements.txt` | Python dependencies needed to run the notebook. |
| `sales_data.csv` | Raw sales transactions (input data). |
| `customer_churn.csv` | Raw customer churn/subscription data (input data). |

## Problem Statement

The business wants to know: who its most valuable customers are, which products/regions drive revenue, how sales trend over time, and whether purchasing activity relates to customer retention.

## Approach

1. **Data collection & exploration** — load both CSVs, check shape, dtypes, missing values, and duplicates.
2. **Data preparation** — defensive missing-value handling, date conversion, and calculated columns (month, weekday, revenue validation, a shared numeric customer key used to merge the two files).
3. **Customer analysis** — top customers by revenue, an estimated customer lifetime value (CLV) using churn-file tenure and monthly charges, and regional revenue distribution.
4. **Sales trend analysis** — monthly revenue trend, best-selling products, weekday patterns.
5. **Pivot tables & retention** — Region x Product and Month x Region pivot tables, overall vs. transacting-customer retention rate, and a contract-type x product crosstab as a cross-sell proxy.
6. **Visualizations** — 5 charts covering trend, ranking, composition, and heatmap chart types.
7. **Executive summary & recommendations** — translated into the report and the notebook's closing section.

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook Sales_Performance_Analysis.ipynb
```

Run all cells top to bottom. Figures are written to `outputs/figures/`.

## Key Findings

- Total recorded revenue: **₹12,365,048** across 100 orders (avg. order value ≈ ₹123,650), Jan 1 – Apr 9, 2024.
- Top region: **North** (32.2% of revenue); weakest: **West** (17.2%).
- Top product: **Laptop** (₹3.89M revenue), more than double the two lowest-performing categories combined.
- Overall customer retention (all 500 customers): **89.4%**. Among the 100 customers who also transacted: **90.0%**.
- **Month-to-month** contract customers churn at **17.1%** — over 6x the rate of **one-year** contract customers (**2.8%**), who also have the highest average order value.

## Data Notes & Limitations

- The two source files use different customer ID formats (`CUST001` vs `C00001`); both encode the same numeric ID, which is what the merge key is built from.
- Each customer in `sales_data.csv` has exactly one recorded transaction, so basket-level cross-selling ("customers who bought X also bought Y") cannot be computed directly from this extract. The notebook uses a contract-type x product crosstab as a proxy and flags this as a data-collection improvement in the recommendations.
- No missing values or duplicate rows were found in either source file; a defensive cleaning step is included regardless, for robustness against future data refreshes.
