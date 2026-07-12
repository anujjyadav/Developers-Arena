# Student Performance Analysis

A comprehensive data analysis pipeline for the **StudentPerformanceFactors** dataset, covering end-to-end exploratory data analysis (EDA), feature engineering, predictive modeling, and automated PDF reporting.

---

## Project Structure

```
week 4 Student Performance Analysis/
├── Student_Performance_Analysis     # Full analysis pipeline
├── requirements.txt                 # Python dependencies
├── StudentPerformanceFactors.csv    # Raw dataset (6,608 records)
├── visualizations/                  # All generated charts (PNG)
│   ├── 01_score_distribution.png
│   ├── 02_correlation_heatmap.png
│   ├── 03_study_patterns.png
│   ├── 04_categorical_analysis.png
│   ├── 05_gender_peers_wellbeing.png
│   ├── 06_feature_importance.png
│   ├── 07_model_comparison.png
│   ├── 08_disability_tutoring.png
│   ├── 09_parental_education_distance.png
│   └── 10_study_efficiency_support.png
└── report/
    └── Student_Performance_Analysis_Report.pdf
```

---

## Dataset

| Feature | Type | Description |
|---|---|---|
| Hours_Studied | Numeric | Weekly study hours |
| Attendance | Numeric | Class attendance % |
| Parental_Involvement | Categorical | Low / Medium / High |
| Access_to_Resources | Categorical | Low / Medium / High |
| Extracurricular_Activities | Categorical | Yes / No |
| Sleep_Hours | Numeric | Nightly sleep hours |
| Previous_Scores | Numeric | Prior academic score |
| Motivation_Level | Categorical | Low / Medium / High |
| Internet_Access | Categorical | Yes / No |
| Tutoring_Sessions | Numeric | Weekly tutoring sessions |
| Family_Income | Categorical | Low / Medium / High |
| Teacher_Quality | Categorical | Low / Medium / High |
| School_Type | Categorical | Public / Private |
| Peer_Influence | Categorical | Negative / Neutral / Positive |
| Physical_Activity | Numeric | Weekly activity hours |
| Learning_Disabilities | Categorical | Yes / No |
| Parental_Education_Level | Categorical | High School / College / Postgraduate |
| Distance_from_Home | Categorical | Near / Moderate / Far |
| Gender | Categorical | Male / Female |
| **Exam_Score** | **Numeric** | **Target variable** |

---

## Pipeline Steps

1. **Data Loading & Validation** — checks file existence, column integrity, empty-dataset guards  
2. **Preprocessing** — median/mode imputation for missing values, duplicate removal  
3. **Feature Engineering** — `Study_Efficiency`, `Support_Score`, `Wellness_Score`, `Score_Category`  
4. **EDA & Visualisation** — 10 publication-quality dark-themed charts  
5. **Predictive Modelling** — Linear, Ridge, Decision Tree, Random Forest, Gradient Boosting  
6. **PDF Report Generation** — automated multi-page report with charts and written insights  

---

## Charts Generated

| # | Chart | Type |
|---|---|---|
| 01 | Exam Score Distribution | Histogram + Bar |
| 02 | Feature Correlation Heatmap | Heatmap |
| 03 | Study Patterns vs Exam Score | Scatter + Line |
| 04 | Categorical Factors Breakdown | Box Plots (6-panel) |
| 05 | Gender, Peers & Wellbeing | Bar + Violin + Scatter |
| 06 | Feature Importances | Horizontal Bar |
| 07 | Model Performance Comparison | Horizontal Bar (3-panel) |
| 08 | Disabilities & Tutoring Sessions | Bar + Line |
| 09 | Parental Education & Distance | Bar (2-panel) |
| 10 | Study Efficiency & Support Score | Scatter + Bar |

---

## Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline
```bash
python main.py
```

### 3. Outputs
- **10 PNG visualizations** → `visualizations/`  
- **PDF report** → `report/Student_Performance_Analysis_Report.pdf`

---

## Key Insights

- **Study hours and attendance** are the strongest numerical predictors of exam performance  
- **Positive peer influence** and **high parental involvement** correlate with higher scores  
- **Learning disabilities** create a measurable score gap that targeted support can narrow  
- **Gradient Boosting** typically achieves the best R² score among the five models tested  
- Engineered `Study_Efficiency` (Hours × Attendance) outperforms either raw variable alone  

---

## Error Handling

The pipeline includes validation at every stage:
- `FileNotFoundError` if the CSV is missing  
- `ValueError` for empty datasets or missing target column  
- Graceful `NaN` handling with fallback imputation strategies  
- All outputs use `os.makedirs(..., exist_ok=True)` for safe directory creation  

---

## Requirements

```
pandas==2.2.2
numpy==1.26.4
matplotlib==3.9.0
seaborn==0.13.2
scikit-learn==1.5.0
scipy==1.13.1
fpdf2==2.7.9
```
