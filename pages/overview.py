"""
Overview Dashboard
"""

import streamlit as st

from utils.load_data import (
    get_kpis,
    get_category_distribution,
    get_inventory,
    get_top_expensive,
    get_cheapest,
    get_discount_analysis
)

from utils.charts import (
    bar_chart,
    pie_chart,
    treemap,
    histogram
)

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Overview Dashboard")

st.markdown("Overall summary of the Zepto product catalog.")

st.divider()

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

kpi = get_kpis()
category = get_category_distribution()
inventory = get_inventory()
discount = get_discount_analysis()
expensive = get_top_expensive()
cheap = get_cheapest()

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Products",
    int(kpi.loc[0, "total_products"])
)

c2.metric(
    "Categories",
    int(kpi.loc[0, "total_categories"])
)

c3.metric(
    "Avg Price",
    f"₹ {kpi.loc[0,'average_selling_price']}"
)

c4.metric(
    "Avg Discount",
    f"{kpi.loc[0,'average_discount']} %"
)

st.divider()

# ----------------------------------------------------
# Products by Category
# ----------------------------------------------------

st.subheader("📦 Products by Category")

fig = bar_chart(
    category,
    x="category",
    y="total_products",
    title="Products by Category",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ----------------------------------------------------
# Category Share
# ----------------------------------------------------

st.subheader("🥧 Category Distribution")

fig = pie_chart(
    category,
    names="category",
    values="total_products",
    title="Category Share"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ----------------------------------------------------
# Inventory
# ----------------------------------------------------

st.subheader("📦 Inventory by Category")

fig = treemap(
    inventory,
    path=["category"],
    values="inventory",
    title="Inventory Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ----------------------------------------------------
# Average Discount
# ----------------------------------------------------

st.subheader("🏷 Average Discount by Category")

fig = bar_chart(
    discount,
    x="category",
    y="average_discount",
    title="Average Discount",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ----------------------------------------------------
# Product Price Distribution
# ----------------------------------------------------

st.subheader("💰 Product Price Distribution")

price_df = expensive.copy()

fig = histogram(
    price_df,
    column="mrp",
    title="MRP Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ----------------------------------------------------
# Top Products
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🔝 Top 10 Expensive Products")

    st.dataframe(
        expensive,
        width='stretch',
        hide_index=True
    )

with right:

    st.subheader("💸 Top 10 Cheapest Products")

    st.dataframe(
        cheap,
        width='stretch',
        hide_index=True
    )

st.divider()

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

st.subheader("📌 Key Insights")

highest_category = category.iloc[0]["category"]
highest_products = category.iloc[0]["total_products"]

highest_inventory = inventory.iloc[0]["category"]

highest_discount = discount.iloc[0]["category"]

st.success(f"""
### Executive Summary

- Total Products: **{int(kpi.loc[0,'total_products']):,}**
- Total Categories: **{int(kpi.loc[0,'total_categories'])}**
- Highest Product Category: **{highest_category}**
- Highest Inventory Category: **{highest_inventory}**
- Highest Average Discount: **{highest_discount}**
- Average Selling Price: **₹ {kpi.loc[0,'average_selling_price']}**
""")