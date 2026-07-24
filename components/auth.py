import sqlite3
from pathlib import Path

DB_PATH = Path("database")
DB_PATH.mkdir(exist_ok=True)

DATABASE = DB_PATH / "healthvibe.db"


def connect():
    return sqlite3.connect(DATABASE)


# ==========================================
# CREATE USERS TABLE
# ==========================================

def create_users_table():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT

    )

    """)

    conn.commit()
    conn.close()


# ==========================================
# REGISTER
# ==========================================

def register(username, password, role):

    conn = connect()
    cur = conn.cursor()

    cur.execute(

        "INSERT INTO users(username,password,role) VALUES(?,?,?)",

        (username, password, role)

    )

    conn.commit()
    conn.close()


# ==========================================
# LOGIN
# ==========================================

def login(username, password):

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,

        (username, password)

    )

    user = cur.fetchone()

    conn.close()

    return user

# ==========================================
# CREATE DEFAULT ADMIN
# ==========================================

def create_default_admin():

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username='admin'"
    )

    user = cur.fetchone()

    if user is None:

        cur.execute(

            """
            INSERT INTO users(username,password,role)
            VALUES(?,?,?)
            """,

            (
                "admin",
                "admin123",
                "Admin"
            )

        )

        conn.commit()

    conn.close()