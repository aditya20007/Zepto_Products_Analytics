"""
load_data.py
------------
Utility functions for loading data from PostgreSQL.
"""

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.database import get_engine
from utils.queries import QUERIES


# =====================================================
# Generic SQL Executor
# =====================================================

@st.cache_data(ttl=600)
def execute_query(query_name):
    """
    Execute SQL query stored in QUERIES dictionary.
    """

    try:
        engine = get_engine()

        if engine is None:
            st.error("❌ Database engine could not be created.")
            return pd.DataFrame()

        query = QUERIES.get(query_name)

        if query is None:
            st.error(f"❌ Query '{query_name}' not found.")
            return pd.DataFrame()

        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        return df

    except Exception as e:
        st.error(f"❌ Database Error:\n\n{e}")
        return pd.DataFrame()


# =====================================================
# Load Complete Dataset
# =====================================================

def load_data():
    return execute_query("all_products")


# =====================================================
# Products
# =====================================================

def get_products():
    return execute_query("all_products")


# =====================================================
# KPI
# =====================================================

def get_kpis():
    return execute_query("kpi")


# =====================================================
# Category Distribution
# =====================================================

def get_category_distribution():
    return execute_query("category_distribution")


def get_product_count():
    return execute_query("category_distribution")


# =====================================================
# Inventory
# =====================================================

def get_inventory():
    return execute_query("inventory")


# =====================================================
# Discount
# =====================================================

def get_discount():
    return execute_query("discount")


def get_discount_analysis():
    return execute_query("discount")


# =====================================================
# Revenue
# =====================================================

def get_revenue():
    return execute_query("revenue")


# =====================================================
# Product Weight
# =====================================================

def get_product_weight():
    return execute_query("all_products")


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