"""
app.py
-------
Main entry point for the Zepto Product Analytics Dashboard.
"""

import streamlit as st

from utils.database import test_connection
from utils.load_data import (
    get_kpis,
    load_data
)

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Zepto Product Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown("""
<style>

[data-testid="stMetric"]{
    background-color:#0000FF; /* Blue metric cards */
    border-radius:12px;
    padding:18px;
    border:1px solid #FF0000; /* Red border */
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.main{
    background-color:#008000; /* Green main background */
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🛒 Zepto Product Analytics Dashboard")

st.markdown("""
Interactive analytics dashboard built using:

- PostgreSQL
- SQL
- Python
- Streamlit
- Plotly
""")

st.divider()

# ---------------------------------------------------
# Database Status
# ---------------------------------------------------

if test_connection():

    st.success("✅ Connected to PostgreSQL Database")

else:

    st.error("❌ Unable to connect to PostgreSQL")

    st.stop()

# ---------------------------------------------------
# Load KPI Data
# ---------------------------------------------------

kpi = get_kpis()

if kpi.empty:

    st.error("No data found.")

    st.stop()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Products",
    int(kpi.loc[0,"total_products"])
)

col2.metric(
    "Categories",
    int(kpi.loc[0,"total_categories"])
)

col3.metric(
    "Average Price",
    f"₹ {kpi.loc[0,'average_selling_price']}"
)

col4.metric(
    "Average Discount",
    f"{kpi.loc[0,'average_discount']} %"
)

col5,col6,col7 = st.columns(3)

col5.metric(
    "Average MRP",
    f"₹ {kpi.loc[0,'average_mrp']}"
)

col6.metric(
    "Inventory",
    f"{int(kpi.loc[0,'total_inventory']):,}"
)

col7.metric(
    "Out Of Stock",
    int(kpi.loc[0,"out_of_stock"])
)

st.divider()

# ---------------------------------------------------
# Dataset Preview
# ---------------------------------------------------

st.subheader("Dataset Preview")

df = load_data()

st.dataframe(
    df.head(20),
    width='stretch',
    hide_index=True
)

# ---------------------------------------------------
# Dataset Information
# ---------------------------------------------------

st.subheader("Dataset Information")

left,right = st.columns(2)

with left:

    st.write("Rows:", df.shape[0])

    st.write("Columns:", df.shape[1])

with right:

    st.write("Duplicate Rows:", df.duplicated().sum())

    st.write("Missing Values:", df.isnull().sum().sum())

st.divider()

# ---------------------------------------------------
# Column Information
# ---------------------------------------------------

st.subheader("Columns")

st.write(list(df.columns))

st.divider()

# ---------------------------------------------------
# Dashboard Pages
# ---------------------------------------------------

st.subheader("Dashboard Pages")

st.markdown("""
Use the **left sidebar** to navigate.

📊 Overview

📦 Product Analysis

💰 Pricing Analysis

📦 Inventory Analysis

💡 Business Insights
""")

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.caption(
    "Developed using PostgreSQL • SQL • Python • Streamlit • Plotly"
)