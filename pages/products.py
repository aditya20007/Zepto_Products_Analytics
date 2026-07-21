import streamlit as st
st.write("PAGE LOADED")
from utils.load_data import (
    get_products,
    get_product_count,
    get_product_weight
)

from utils.charts import (
    bar_chart,
    histogram
)

st.set_page_config(
    page_title="Products",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Analysis")

st.markdown("Explore products, categories and inventory.")

st.divider()

# ------------------------------------------------
# Load Data
# ------------------------------------------------

df = get_products()
category = get_product_count()
weight = get_product_weight()

# ------------------------------------------------
# Sidebar Filters
# ------------------------------------------------

st.sidebar.header("Filters")

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

search = st.sidebar.text_input(
    "Search Product"
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ------------------------------------------------
# KPIs
# ------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Products",
    len(filtered_df)
)

c2.metric(
    "Categories",
    filtered_df["category"].nunique()
)

c3.metric(
    "Average Price",
    f"₹ {filtered_df['discountedsellingprice'].mean():.2f}"
)

st.divider()

# ------------------------------------------------
# Product Table
# ------------------------------------------------

st.subheader("📋 Product List")

st.dataframe(
    filtered_df,
    width='stretch',
    hide_index=True
)

# ------------------------------------------------
# Products by Category
# ------------------------------------------------

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

# ------------------------------------------------
# Product Weight Distribution
# ------------------------------------------------

st.subheader("⚖️ Weight Distribution")

fig = histogram(
    weight,
    column="weightingms",
    title="Product Weight Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ------------------------------------------------
# Most Expensive Products
# ------------------------------------------------

st.subheader("💰 Top 10 Expensive Products")

top = filtered_df.nlargest(10, "mrp")[
    [
        "name",
        "category",
        "mrp",
        "discountedsellingprice"
    ]
]

st.dataframe(
    top,
    width='stretch',
    hide_index=True
)

# ------------------------------------------------
# Cheapest Products
# ------------------------------------------------

st.subheader("💸 Top 10 Cheapest Products")

cheap = filtered_df.nsmallest(
    10,
    "discountedsellingprice"
)[
    [
        "name",
        "category",
        "discountedsellingprice"
    ]
]

st.dataframe(
    cheap,
    width='stretch',
    hide_index=True
)

st.divider()

st.success(f"""
### Product Summary

- Total Products: **{len(filtered_df)}**
- Categories: **{filtered_df['category'].nunique()}**
- Average Selling Price: **₹ {filtered_df['discountedsellingprice'].mean():.2f}**
- Average MRP: **₹ {filtered_df['mrp'].mean():.2f}**
""")