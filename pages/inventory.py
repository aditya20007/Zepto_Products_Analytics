import streamlit as st

from utils.load_data import (
    get_inventory,
    get_low_stock,
    get_out_of_stock,
    load_data
)

from utils.charts import (
    bar_chart,
    pie_chart,
    histogram
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Inventory Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Analysis")

st.markdown(
    "Monitor inventory levels, stock availability, and category-wise inventory."
)

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------

df = load_data()

inventory = get_inventory()

low_stock = get_low_stock()

out_stock = get_out_of_stock()

# -------------------------------------------------
# Sidebar Filter
# -------------------------------------------------

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

if selected_category != "All":
    df = df[df["category"] == selected_category]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

total_inventory = int(df["availablequantity"].sum())

total_products = len(df)

low_stock_count = len(df[df["availablequantity"] < 10])

out_stock_count = len(df[df["outofstock"] == True])

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Inventory",
    f"{total_inventory:,}"
)

col2.metric(
    "Products",
    total_products
)

col3.metric(
    "Low Stock",
    low_stock_count
)

col4.metric(
    "Out Of Stock",
    out_stock_count
)

st.divider()

# -------------------------------------------------
# Inventory by Category
# -------------------------------------------------

st.subheader("📦 Inventory by Category")

fig = bar_chart(
    inventory,
    x="category",
    y="inventory",
    title="Inventory by Category",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Inventory Share
# -------------------------------------------------

st.subheader("🥧 Inventory Share")

fig = pie_chart(
    inventory,
    names="category",
    values="inventory",
    title="Inventory Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Quantity Distribution
# -------------------------------------------------

st.subheader("📊 Available Quantity Distribution")

fig = histogram(
    df,
    column="availablequantity",
    title="Inventory Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------
# Low Stock Products
# -------------------------------------------------

st.subheader("⚠️ Low Stock Products")

if low_stock.empty:

    st.success("No low stock products found.")

else:

    st.dataframe(
        low_stock,
        width='stretch',
        hide_index=True
    )

# -------------------------------------------------
# Out Of Stock Products
# -------------------------------------------------

st.subheader("❌ Out Of Stock Products")

if out_stock.empty:

    st.success("No out-of-stock products.")

else:

    st.dataframe(
        out_stock,
        width='stretch',
        hide_index=True
    )

# -------------------------------------------------
# Inventory Dataset
# -------------------------------------------------

st.subheader("📋 Inventory Details")

inventory_columns = [
    "sku_id",
    "name",
    "category",
    "availablequantity",
    "outofstock"
]

st.dataframe(
    df[inventory_columns],
    width='stretch',
    hide_index=True
)

# -------------------------------------------------
# Business Insights
# -------------------------------------------------

highest_inventory = inventory.iloc[0]

st.subheader("💡 Inventory Insights")

st.success(f"""
### Inventory Summary

📦 Highest Inventory Category:
**{highest_inventory['category']}**

Inventory:
**{highest_inventory['inventory']:,} Units**

---

📊 Total Inventory:
**{total_inventory:,} Units**

---

⚠️ Low Stock Products:
**{low_stock_count}**

---

❌ Out Of Stock Products:
**{out_stock_count}**
""")

# -------------------------------------------------
# Recommendations
# -------------------------------------------------

st.subheader("🚀 Recommendations")

recommendations = []

if low_stock_count > 0:
    recommendations.append(
        "Replenish products with inventory below 10 units."
    )

if out_stock_count > 0:
    recommendations.append(
        "Restock out-of-stock products immediately."
    )

recommendations.append(
    f"Maintain inventory levels for '{highest_inventory['category']}' based on demand."
)

for i, rec in enumerate(recommendations, start=1):
    st.info(f"Recommendation {i}: {rec}")

# -------------------------------------------------
# Download Report
# -------------------------------------------------

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Inventory Report",
    data=csv,
    file_name="inventory_report.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "Built using PostgreSQL • SQL • Python • Streamlit • Plotly"
)