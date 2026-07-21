"""
queries.py
----------
All SQL queries used by the dashboard.
"""

QUERIES = {


"savings": """

SELECT
    sku_id,
    name,
    category,
    mrp,
    discountedsellingprice,
    (mrp - discountedsellingprice) AS savings

FROM zepto

ORDER BY savings DESC

LIMIT 10;

""",

# =====================================================
# LOAD COMPLETE DATASET
# =====================================================

"all_products": """

SELECT
    sku_id,
    category,
    name,
    mrp,
    discountpercent,
    availablequantity,
    discountedsellingprice,
    weightingms,
    outofstock,
    quantity
FROM zepto;

""",

# =====================================================
# KPI
# =====================================================

"kpi": """

SELECT

COUNT(*) AS total_products,

COUNT(DISTINCT category) AS total_categories,

ROUND(AVG(mrp),2) AS average_mrp,

ROUND(AVG(discountedsellingprice),2) AS average_selling_price,

ROUND(AVG(discountpercent),2) AS average_discount,

SUM(availablequantity) AS total_inventory,

SUM(
CASE
WHEN outofstock = TRUE
THEN 1
ELSE 0
END
) AS out_of_stock

FROM zepto;

""",

# =====================================================
# CATEGORY DISTRIBUTION
# =====================================================

"category_distribution": """

SELECT

category,

COUNT(*) AS total_products

FROM zepto

GROUP BY category

ORDER BY total_products DESC;

""",

# =====================================================
# INVENTORY
# =====================================================

"inventory": """

SELECT

category,

SUM(availablequantity) AS inventory

FROM zepto

GROUP BY category

ORDER BY inventory DESC;

""",

# =====================================================
# DISCOUNT
# =====================================================

"discount": """

SELECT

category,

ROUND(AVG(discountpercent),2) AS average_discount

FROM zepto

GROUP BY category

ORDER BY average_discount DESC;

""",

# =====================================================
# REVENUE
# =====================================================

"revenue": """

SELECT

category,

SUM(discountedsellingprice * availablequantity)

AS revenue

FROM zepto

GROUP BY category

ORDER BY revenue DESC;

""",

# =====================================================
# TOP EXPENSIVE
# =====================================================

"top_expensive": """

SELECT

sku_id,

name,

category,

mrp,

discountedsellingprice

FROM zepto

ORDER BY mrp DESC

LIMIT 10;

""",

# =====================================================
# CHEAPEST
# =====================================================

"top_cheapest": """

SELECT

sku_id,

name,

category,

discountedsellingprice

FROM zepto

ORDER BY discountedsellingprice

LIMIT 10;

""",

# =====================================================
# TOP DISCOUNT
# =====================================================

"top_discount": """

SELECT

sku_id,

name,

category,

discountpercent

FROM zepto

ORDER BY discountpercent DESC

LIMIT 10;

""",

# =====================================================
# OUT OF STOCK
# =====================================================

"out_of_stock": """

SELECT

sku_id,

name,

category,

availablequantity

FROM zepto

WHERE outofstock = TRUE;

""",

# =====================================================
# LOW STOCK
# =====================================================

"low_stock": """

SELECT

sku_id,

name,

category,

availablequantity

FROM zepto

WHERE availablequantity < 10

ORDER BY availablequantity;

""",

# =====================================================
# BUSINESS SUMMARY
# =====================================================

"business_summary": """

SELECT

category,

COUNT(*) AS total_products,

ROUND(AVG(discountedsellingprice),2)

AS average_price,

ROUND(AVG(discountpercent),2)

AS average_discount,

SUM(availablequantity)

AS inventory,

SUM(

discountedsellingprice

*

availablequantity

)

AS revenue

FROM zepto

GROUP BY category

ORDER BY revenue DESC;

"""

}