"""
database.py
-----------
Creates and manages PostgreSQL database connection.
"""

import os
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()


def get_config(key):
    """Read from Streamlit Secrets first, then .env"""
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)


DB_USER = get_config("DB_USER")
DB_PASSWORD = get_config("DB_PASSWORD")
DB_HOST = get_config("DB_HOST")
DB_PORT = get_config("DB_PORT")
DB_NAME = get_config("DB_NAME")


@st.cache_resource
def get_engine():

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )

    return engine


def test_connection():

    try:
        engine = get_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True

    except Exception as e:
        st.error(e)
        return False