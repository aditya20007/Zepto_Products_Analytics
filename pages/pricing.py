import streamlit as st
import pandas as pd

from utils.load_data import (
    load_data,
    get_discount,
    get_top_discount,
    get_revenue
)

from utils.charts import (
    histogram,
    bar_chart,
    scatter_chart,
    box_plot
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Pricing Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Pricing Analysis")

st.markdown(
    "Analyze product pricing, discounts and revenue."
)

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------

df = load_data()

discount = get_discount()

top_discount = get_top_discount()

revenue = get_revenue()

# -------------------------------------------------
# Sidebar Filter
# -------------------------------------------------

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

selected = st.sidebar.selectbox(
    "Category",
    categories
)

if selected != "All":
    df = df[df["category"] == selected]

# -------------------------------------------------
# KPIs
# -------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Average MRP",
    f"₹ {df['mrp'].mean():.2f}"
)

c2.metric(
    "Average Selling Price",
    f"₹ {df['discountedsellingprice'].mean():.2f}"
)

c3.metric(
    "Average Discount",
    f"{df['discountpercent'].mean():.2f}%"
)

c4.metric(
    "Products",
    len(df)
)

st.divider()

# -------------------------------------------------
# Histogram
# -------------------------------------------------

st.subheader("MRP Distribution")

fig = histogram(
    df,
    "mrp",
    "MRP Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Scatter Plot
# -------------------------------------------------

st.subheader("MRP vs Selling Price")

fig = scatter_chart(
    df,
    x="mrp",
    y="discountedsellingprice",
    title="MRP vs Selling Price",
    color="category",
    size="discountpercent"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Box Plot
# -------------------------------------------------

st.subheader("Selling Price by Category")

fig = box_plot(
    df,
    x="category",
    y="discountedsellingprice",
    title="Selling Price Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Average Discount
# -------------------------------------------------

st.subheader("Average Discount by Category")

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

# -------------------------------------------------
# Revenue
# -------------------------------------------------

st.subheader("Estimated Revenue")

fig = bar_chart(
    revenue,
    x="category",
    y="revenue",
    title="Revenue by Category",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Top Discount Products
# -------------------------------------------------

st.subheader("Top 10 Highest Discount Products")

st.dataframe(
    top_discount,
    width='stretch',
    hide_index=True
)

# -------------------------------------------------
# Biggest Savings
# -------------------------------------------------

st.subheader("Products with Highest Savings")

df["savings"] = (
    df["mrp"] -
    df["discountedsellingprice"]
)

saving = df.nlargest(
    10,
    "savings"
)[
[
    "name",
    "category",
    "mrp",
    "discountedsellingprice",
    "savings"
]
]

st.dataframe(
    saving,
    width='stretch',
    hide_index=True
)

# -------------------------------------------------
# Download CSV
# -------------------------------------------------

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Pricing Data",
    csv,
    file_name="pricing_analysis.csv",
    mime="text/csv"
)

st.divider()

st.success(f"""

### Pricing Insights

• Average MRP: ₹ **{df['mrp'].mean():.2f}**

• Average Selling Price: ₹ **{df['discountedsellingprice'].mean():.2f}**

• Average Discount: **{df['discountpercent'].mean():.2f}%**

• Highest Discount Category:
**{discount.iloc[0]['category']}**

• Highest Revenue Category:
**{revenue.iloc[0]['category']}**

""")