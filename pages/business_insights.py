import streamlit as st
st.write("PAGE LOADED")
from utils.load_data import (
    get_business_summary,
    get_revenue,
    get_discount,
    get_inventory,
    get_low_stock,
    get_out_of_stock,
    get_top_expensive,
    get_top_discount
)

from utils.charts import (
    bar_chart,
    pie_chart
)

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Business Insights",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Business Insights Dashboard")

st.markdown(
    "Business recommendations generated from PostgreSQL analytics."
)

st.divider()

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

summary = get_business_summary()
revenue = get_revenue()
discount = get_discount()
inventory = get_inventory()
low_stock = get_low_stock()
out_stock = get_out_of_stock()
expensive = get_top_expensive()
top_discount = get_top_discount()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Categories",
    len(summary)
)

col2.metric(
    "Low Stock Products",
    len(low_stock)
)

col3.metric(
    "Out of Stock",
    len(out_stock)
)

col4.metric(
    "Highest Revenue",
    revenue.iloc[0]["category"]
)

st.divider()

# -------------------------------------------------------
# Revenue Analysis
# -------------------------------------------------------

st.subheader("💰 Revenue by Category")

fig = bar_chart(
    revenue,
    x="category",
    y="revenue",
    title="Estimated Revenue by Category",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------------
# Discount Analysis
# -------------------------------------------------------

st.subheader("🏷️ Average Discount")

fig = bar_chart(
    discount,
    x="category",
    y="average_discount",
    title="Average Discount by Category",
    color="category"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------------
# Inventory Share
# -------------------------------------------------------

st.subheader("📦 Inventory Distribution")

fig = pie_chart(
    inventory,
    names="category",
    values="inventory",
    title="Inventory Share"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# -------------------------------------------------------
# Business Summary Table
# -------------------------------------------------------

st.subheader("📋 Business Summary")

st.dataframe(
    summary,
    width='stretch',
    hide_index=True
)

# -------------------------------------------------------
# Executive Insights
# -------------------------------------------------------

highest_revenue = revenue.iloc[0]
highest_discount = discount.iloc[0]
highest_inventory = inventory.iloc[0]

st.subheader("📈 Executive Insights")

st.success(f"""
### Key Business Insights

💰 Highest Revenue Category:
**{highest_revenue['category']}**

Estimated Revenue:
**₹ {highest_revenue['revenue']:,.2f}**

---

🏷️ Highest Discount Category:
**{highest_discount['category']}**

Average Discount:
**{highest_discount['average_discount']}%**

---

📦 Highest Inventory Category:
**{highest_inventory['category']}**

Inventory:
**{highest_inventory['inventory']:,} Units**

---

⚠️ Low Stock Products:
**{len(low_stock)}**

❌ Out of Stock Products:
**{len(out_stock)}**
""")

# -------------------------------------------------------
# Recommendations
# -------------------------------------------------------

st.subheader("🚀 Business Recommendations")

recommendations = []

if len(out_stock) > 0:
    recommendations.append(
        "Restock out-of-stock products to avoid revenue loss."
    )

if len(low_stock) > 0:
    recommendations.append(
        "Monitor low-stock products and replenish inventory."
    )

recommendations.append(
    f"Increase promotions for '{highest_revenue['category']}' to maximize revenue."
)

recommendations.append(
    f"Review pricing strategy for '{highest_discount['category']}' due to high discounts."
)

recommendations.append(
    f"Optimize inventory allocation for '{highest_inventory['category']}'."
)

for i, rec in enumerate(recommendations, start=1):
    st.info(f"**Recommendation {i}:** {rec}")

# -------------------------------------------------------
# Top Products
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("💎 Top 10 Expensive Products")

    st.dataframe(
        expensive,
        width='stretch',
        hide_index=True
    )

with right:

    st.subheader("🔥 Top Discount Products")

    st.dataframe(
        top_discount,
        width='stretch',
        hide_index=True
    )

st.divider()

# -------------------------------------------------------
# Download Report
# -------------------------------------------------------

csv = summary.to_csv(index=False)

st.download_button(
    label="📥 Download Business Report",
    data=csv,
    file_name="business_summary.csv",
    mime="text/csv"
)

st.caption(
    "Built with PostgreSQL • SQL • Python • Streamlit • Plotly"
)