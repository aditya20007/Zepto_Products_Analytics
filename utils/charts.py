"""
charts.py
---------
Reusable Plotly chart functions for the Zepto Product Analytics Dashboard.
"""
import os

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.database import get_engine
from utils.load_data import execute_query
from utils.queries import QUERIES
import plotly.express as px
import plotly.graph_objects as go

def get_products():
    return execute_query("all_products")

def get_product_count():
    return execute_query("category_distribution")

def get_product_weight():
    return execute_query("all_products")

def get_discount_analysis():
    return execute_query("discount")
# ==========================================================
# Common Layout
# ==========================================================

def update_layout(fig, title):

    fig.update_layout(
        title=title,
        template="plotly_white",
        title_x=0.5,
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title=""
    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(df, x, y, title, color=None):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        text_auto=True
    )

    return update_layout(fig, title)


# ==========================================================
# HORIZONTAL BAR
# ==========================================================

def horizontal_bar(df, x, y, title, color=None):

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        text_auto=True
    )

    return update_layout(fig, title)


# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(df, names, values, title):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.45
    )

    return update_layout(fig, title)


# ==========================================================
# DONUT CHART
# ==========================================================

def donut_chart(df, names, values, title):

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df[names],
                values=df[values],
                hole=0.60
            )
        ]
    )

    return update_layout(fig, title)


# ==========================================================
# LINE CHART
# ==========================================================

def line_chart(df, x, y, title):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True
    )

    return update_layout(fig, title)


# ==========================================================
# SCATTER PLOT
# ==========================================================

def scatter_chart(df, x, y, title, color=None, size=None):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_data=df.columns
    )

    return update_layout(fig, title)


# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram(df, column, title):

    fig = px.histogram(
        df,
        x=column,
        nbins=30
    )

    return update_layout(fig, title)


# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(df, x, y, title):

    fig = px.box(
        df,
        x=x,
        y=y,
        color=x
    )

    return update_layout(fig, title)


# ==========================================================
# TREEMAP
# ==========================================================

def treemap(df, path, values, title):

    fig = px.treemap(
        df,
        path=path,
        values=values
    )

    return update_layout(fig, title)


# ==========================================================
# HEATMAP
# ==========================================================

def heatmap(df, x, y, z, title):

    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
        z=z
    )

    return update_layout(fig, title)


# ==========================================================
# AREA CHART
# ==========================================================

def area_chart(df, x, y, title):

    fig = px.area(
        df,
        x=x,
        y=y
    )

    return update_layout(fig, title)


# ==========================================================
# BUBBLE CHART
# ==========================================================

def bubble_chart(df, x, y, size, color, title):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name="name"
    )

    return update_layout(fig, title)