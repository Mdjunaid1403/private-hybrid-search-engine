
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    neon_database_url = os.getenv("NEON_DATABASE_URL")

    if neon_database_url:
        return psycopg.connect(neon_database_url)

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )
