# Metro Rail Ridership Forecasting

A machine learning-based dashboard for analyzing metro ridership, forecasting passenger demand, evaluating models, and supporting train capacity planning.

## Project Overview

This project demonstrates an end-to-end metro ridership forecasting workflow using synthetic demonstration data.

**Important:** This is synthetic data, not official Chennai Metro Rail Limited operational data.

## Project Objectives

- Analyze historical daily ridership.
- Compare ridership across metro lines.
- Forecast passenger demand.
- Compare forecasting models.
- Identify important forecasting features.
- Estimate train frequency and headway.
- Validate dataset quality.

## Technologies Used

- Python 3.11
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- LightGBM
- Plotly
- Streamlit
- Joblib
- Jupyter Notebook

## Machine Learning Models

1. Seasonal Naive
2. SARIMAX
3. LightGBM

## Model Performance

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| SARIMAX | 10,333.29 | 20,004.86 | 2.50% |
| LightGBM | 13,477.23 | 21,268.51 | 3.34% |
| Seasonal Naive | 26,223.62 | 59,703.64 | 6.76% |

SARIMAX achieved the lowest error in the project's backtesting results.

## Dashboard Pages

1. Overview
2. Ridership Analysis
3. Line Analysis
4. Forecasting
5. Model Performance
6. Explainability
7. Capacity Planning

## Capacity Planning

The capacity planning module estimates:
- Peak Hour Peak Direction Traffic (PHPDT)
- Required trains per hour
- Required headway in minutes

Demonstration assumptions:
- Peak hour share: 10%
- Peak direction share: 60%
- Train capacity: 1,200 passengers

These are project assumptions, not verified operational specifications.

## Project Structure

```text
PROJECT_METRO/
|-- app/
|   |-- Home.py
|   |-- utils.py
|   |-- calculations.py
|   |-- components.py
|   |-- charts.py
|   |-- pages/
|       |-- 1_Ridership_Analysis.py
|       |-- 2_Line_Analysis.py
|       |-- 3_Forecasting.py
|       |-- 4_Model_Performance.py
|       |-- 5_Explainability.py
|       |-- 6_Capacity_Planning.py
|-- models/
|   |-- metro_ridership_lightgbm.pkl
|-- outputs/
|-- metro_daily_ridership.csv
|-- metro_ridership_forecasting.ipynb
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd PROJECT_METRO
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app/Home.py
```

## Forecast Period

The included demonstration forecast covers July 1, 2025 to July 28, 2025. It is not a live forecast.

## Limitations

- The dataset is synthetic demonstration data.
- Forecast performance depends on the dataset and evaluation period.
- Capacity calculations use simplified assumptions.
- Results should not be used for actual metro operational decisions.

## Author

**Santhosh C**

Machine Learning and Data Analytics Project
