import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path("database")
DB_PATH.mkdir(exist_ok=True)

DATABASE = DB_PATH / "healthvibe.db"


def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ===========================
# PASSWORD HASH
# ===========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ===========================
# CREATE USERS TABLE
# ===========================

def create_users_table():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ===========================
# REGISTER
# ===========================

def register_user(full_name, email, password, role):

    conn = connect()
    cur = conn.cursor()

    try:

        cur.execute("""

        INSERT INTO users(

            full_name,
            email,
            password,
            role

        )

        VALUES(?,?,?,?)

        """, (

            full_name,
            email,
            hash_password(password),
            role

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ===========================
# LOGIN
# ===========================

def login_user(email, password):

    conn = connect()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM users

    WHERE email=?
    AND password=?

    """, (

        email,
        hash_password(password)

    ))

    user = cur.fetchone()

    conn.close()

    return user