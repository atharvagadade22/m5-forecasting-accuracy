# Retail Inventory Optimization

This project explores demand forecasting and inventory optimization using the
M5 Forecasting data. It includes analysis notebooks and a Streamlit dashboard
for comparing forecasts with actual sales and reviewing inventory policies,
including safety stock and reorder points.

## Project files

- `Inventory_Optimization_Pipeline.ipynb` - forecasting and inventory pipeline
- `notebooks/EDA.ipynb` - exploratory data analysis
- `notebooks/Experiments.ipynb` - model experiments
- `app.py` - Streamlit dashboard

## Run the dashboard

Install the dashboard dependencies:

```bash
python -m pip install streamlit pandas plotly
```

Place the generated `inventory_dashboard_data.csv` and `daily_forecasts.csv`
files in the project root, then run:

```bash
streamlit run app.py
```

## Data

Dataset files and generated CSV outputs are excluded from this repository.
Obtain the M5 source data separately and run the pipeline notebooks to generate
the CSV files required by the dashboard.
