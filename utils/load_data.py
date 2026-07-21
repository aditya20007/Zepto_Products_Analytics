"""
load_data.py
------------
Utility functions for loading data from PostgreSQL.
"""

import os

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.database import get_engine
from utils.queries import QUERIES

print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_PORT =", os.getenv("DB_PORT"))
print("DB_NAME =", os.getenv("DB_NAME"))
print("DB_USER =", os.getenv("DB_USER"))
print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))

# =====================================================
# Generic SQL Executor
# =====================================================
# =====================================================
# Products (full dataset with details)
# =====================================================

def get_products():

    return execute_query("all_products")


# =====================================================
# Product Count by Category
# =====================================================

def get_product_count():

    return execute_query("category_distribution")


# =====================================================
# Product Weight Data
# =====================================================

def get_product_weight():

    return execute_query("all_products")


# =====================================================
# Discount Analysis (alias used by overview page)
# =====================================================

def get_discount_analysis():

    return execute_query("discount")

@st.cache_data(ttl=600)
def execute_query(query_name):
    """
    Execute a SQL query stored in QUERIES dictionary.

    Example:
        execute_query("kpi")
        execute_query("inventory")
    """

    try:

        engine = get_engine()

        if engine is None:
            return pd.DataFrame()

        query = QUERIES.get(query_name)

        if query is None:
            st.error(f"Query '{query_name}' not found.")
            return pd.DataFrame()

        with engine.connect() as conn:

            df = pd.read_sql(
                text(query),
                conn
            )

        return df

    except Exception as e:

        st.error(f"Database Error:\n\n{e}")

        return pd.DataFrame()


# =====================================================
# Load Complete Dataset
# =====================================================

def load_data():

    return execute_query("all_products")


# =====================================================
# Dashboard KPI
# =====================================================

def get_kpis():

    return execute_query("kpi")


# =====================================================
# Category Distribution
# =====================================================

def get_category_distribution():

    return execute_query("category_distribution")


# =====================================================
# Inventory
# =====================================================

def get_inventory():

    return execute_query("inventory")


# =====================================================
# Discount Analysis
# =====================================================

def get_discount():

    return execute_query("discount")


# =====================================================
# Revenue Analysis
# =====================================================

def get_revenue():

    return execute_query("revenue")


# =====================================================
# Top Expensive Products
# =====================================================

def get_top_expensive():

    return execute_query("top_expensive")


# =====================================================
# Cheapest Products
# =====================================================

def get_cheapest():

    return execute_query("top_cheapest")


# =====================================================
# Highest Discount Products
# =====================================================

def get_top_discount():

    return execute_query("top_discount")


# =====================================================
# Low Stock Products
# =====================================================

def get_low_stock():

    return execute_query("low_stock")


# =====================================================
# Out Of Stock Products
# =====================================================

def get_out_of_stock():

    return execute_query("out_of_stock")


# =====================================================
# Business Summary
# =====================================================

def get_business_summary():

    return execute_query("business_summary")