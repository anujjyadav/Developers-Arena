# Sales Analysis Project

## Project Overview

This project performs Exploratory Data Analysis (EDA) on a sales dataset
to understand business performance across products, regions, and time.
The notebook cleans the data, computes key business metrics, and
generates insights to support decision-making.

------------------------------------------------------------------------

## Objectives

-   Analyze overall sales performance.
-   Identify the best-selling product.
-   Compare revenue across regions.
-   Analyze monthly revenue trends.
-   Generate actionable business insights and recommendations.

------------------------------------------------------------------------

## Dataset

**File:** `sales_data.csv`

The dataset contains sales transactions from **January to April 2024**.

Main columns include: - Date - Product - Region - Quantity - Unit
Price - Revenue

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Jupyter Notebook
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn

------------------------------------------------------------------------

## Project Structure

    Sales-Analysis/
    │── sales_analysis.ipynb
    │── sales_data.csv
    │── analysis_report.md
    │── README.md

------------------------------------------------------------------------

## Analysis Performed

-   Data loading and inspection
-   Missing value and duplicate check
-   Feature engineering (Month extraction)
-   Revenue analysis by product
-   Revenue analysis by region
-   Monthly sales trend analysis
-   Business insights and recommendations

------------------------------------------------------------------------

## Key Findings

-   Laptop generated the highest revenue (31.5%).
-   North region contributed the highest revenue (32.2%).
-   March 2024 recorded the highest monthly revenue.
-   Headphones showed high average price but comparatively lower sales
    volume.
-   West region has strong growth potential.

------------------------------------------------------------------------

## Business Recommendations

-   Maintain sufficient inventory of laptops.
-   Improve marketing for headphones.
-   Increase focus on the West region.
-   Investigate the decline in April sales.

------------------------------------------------------------------------

## How to Run

1.  Clone the repository.
2.  Install the required libraries.

``` bash
pip install pandas numpy matplotlib seaborn
```

3.  Open the notebook.

``` bash
jupyter notebook sales_analysis.ipynb
```

4.  Run all cells to reproduce the analysis.

------------------------------------------------------------------------

## Output

The project produces: - Summary statistics - Product-wise revenue
analysis - Region-wise revenue analysis - Monthly sales trends -
Business insights - A detailed analysis report

------------------------------------------------------------------------

## Future Improvements

-   Build an interactive dashboard using Power BI or Streamlit.
-   Add sales forecasting using Machine Learning.
-   Include customer segmentation and profitability analysis.

------------------------------------------------------------------------

## Author

Anuj Yadav

