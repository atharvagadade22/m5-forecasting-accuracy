import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup the Web Page
st.set_page_config(page_title="Inventory ML Dashboard", layout="wide")
st.title("Retail Inventory Optimization Dashboard")

# 2. Load the Data
@st.cache_data
def load_data():
    inv_df = pd.read_csv('inventory_dashboard_data.csv')
    sales_df = pd.read_csv('daily_forecasts.csv')
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    return inv_df, sales_df

inv_policy, daily_sales = load_data()

# 3. Create the Layout (Sidebar for Calendar, Main Area for Tables/Graphs)
st.sidebar.header("Filter by Date & Item")

# CALENDAR COMPONENT: Let user pick a date range
min_date = daily_sales['date'].min().date()
max_date = daily_sales['date'].min().date() + pd.Timedelta(days=27)

selected_dates = st.sidebar.date_input(
    "Select Forecast Horizon (Calendar)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ITEM SELECTOR
item_list = inv_policy['id'].unique().tolist()
selected_item = st.sidebar.selectbox("Search for a specific Item:", ["All Items"] + item_list)

# 4. Filter the data based on user input
if selected_item != "All Items":
    inv_policy = inv_policy[inv_policy['id'] == selected_item]
    daily_sales = daily_sales[daily_sales['id'] == selected_item]

# 5. Top KPI Metrics
st.subheader("Financial Impact (28-Day Horizon)")
col1, col2, col3 = st.columns(3)
col1.metric("Total ML Inventory Cost", f"${inv_policy['ml_total_cost'].sum():,.2f}")
col2.metric("Baseline Inventory Cost", f"${inv_policy['naive_total_cost'].sum():,.2f}")
col3.metric("Total Money Saved by ML", f"${(inv_policy['naive_total_cost'].sum() - inv_policy['ml_total_cost'].sum()):,.2f}", delta="Cost Reduction")

# 6. Interactive Forecast Chart
st.subheader("📅 Daily Sales Forecast vs Actual")
# Group by date to show total sales trends
daily_summary = daily_sales.groupby('date')[['sales', 'predicted_sales']].sum().reset_index()

fig = px.line(daily_summary, x='date', y=['sales', 'predicted_sales'],
              labels={'value': 'Units Sold', 'date': 'Calendar Date', 'variable': 'Legend'},
              title="Predicted vs Actual Demand Trend")
st.plotly_chart(fig, use_container_width=True)

# 7. Interactive Data Table
st.subheader("Executable Inventory Policy (Action Items for Manager)")
st.markdown("This table shows the exact **Safety Stock** and **Reorder Point (ROP)** for each item based on ML predictions.")

# Clean up column names for the web display
display_df = inv_policy[['id', 'actual_28d_sales', 'ml_forecast_28d', 'ml_safety_stock', 'ml_ROP']].copy()
display_df.columns = ['Item ID', 'Actual Sales', 'ML Forecast', 'Safety Stock (Units)', 'Reorder Point (ROP)']

# Display as an interactive web table
st.dataframe(display_df, use_container_width=True, height=300)