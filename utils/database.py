"""
database.py
-----------
Creates and manages PostgreSQL database connection.
"""

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()


DB_USER = "postgres"
DB_PASSWORD = "@Mahi2040"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "zepto_sql_project"
@st.cache_resource
def get_engine():

    try:

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


    except Exception as e:
        print("Database Engine Error:", e)
        return None



def test_connection():

    print("Testing PostgreSQL connection...")

    try:

        engine = get_engine()

        if engine is None:
            return False


        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print(result.fetchone())


        print("✅ PostgreSQL Connected Successfully!")
        return True


    except Exception as e:
        print("❌ Connection Error:")
        print(e)
        return False