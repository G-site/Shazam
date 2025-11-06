import os
from dotenv import load_dotenv
import psycopg  # psycopg3
from psycopg.rows import dict_row

load_dotenv()
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


# Пул соединений
pool: psycopg.AsyncConnection | None = None


async def connect():
    global pool
    try:
        pool = await psycopg.AsyncConnection.connect(
            host=HOST,
            port=PORT,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            autocommit=True,  # для простоты
            row_factory=dict_row,  # чтобы получать словари вместо кортежей
            sslmode='require'  # для Supabase
        )
        print("Connected to DB")
    except Exception as e:
        print("Failed to connect to DB:", e)


async def set_user(id, username, name):
    if pool is None:
        raise RuntimeError("DB pool is not initialized")
    async with pool.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO users (id, username, name)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """,
            (id, username, name)
        )


async def check_admin(id):
    if pool is None:
        raise RuntimeError("DB pool is not initialized")

    async with pool.cursor() as cur:
        await cur.execute(
            "SELECT status FROM users WHERE id = %s;",
            (id,)
        )
        row = await cur.fetchone()
        return row["status"] if row else None


async def get_all_users():
    if pool is None:
        raise RuntimeError("DB pool is not initialized")

    async with pool.cursor() as cur:
        await cur.execute("SELECT id FROM users;")
        rows = await cur.fetchall()
        return [row["id"] for row in rows]


async def get_name_by_id(id):
    if pool is None:
        raise RuntimeError("DB pool is not initialized")

    async with pool.cursor() as cur:
        await cur.execute("SELECT name FROM users WHERE id = %s;", (id,))
        row = await cur.fetchone()
        return row["name"] if row else None
