import sqlite3
import bcrypt
from pathlib import Path

# =====================================================
# DATABASE CONFIG
# =====================================================

DB_FOLDER = Path("database")
DB_FOLDER.mkdir(exist_ok=True)

DATABASE = DB_FOLDER / "healthvibe.db"


# =====================================================
# CONNECTION
# =====================================================

def connect():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# =====================================================
# PASSWORD
# =====================================================

def hash_password(password: str) -> str:

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# =====================================================
# CREATE TABLE
# =====================================================

def create_users_table():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()
    conn.close()


# =====================================================
# REGISTER
# =====================================================

def register(username, password, role):

    username = username.strip()
    password = password.strip()

    if username == "":
        return False, "Username is required."

    if password == "":
        return False, "Password is required."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=?",
        (username,)
    )

    existing = cur.fetchone()

    if existing:

        conn.close()

        return False, "Username already exists."

    hashed = hash_password(password)

    cur.execute(
        """
        INSERT INTO users(
            username,
            password,
            role
        )
        VALUES(?,?,?)
        """,
        (
            username,
            hashed,
            role
        )
    )

    conn.commit()
    conn.close()

    return True, "User registered successfully."

    # =====================================================
# LOGIN
# =====================================================

def login(username, password):

    username = username.strip()
    password = password.strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cur.fetchone()

    conn.close()

    if user is None:
        return None

    if verify_password(password, user["password"]):
        return user

    return None


# =====================================================
# DEFAULT ADMIN
# =====================================================

def create_default_admin():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    admin = cur.fetchone()

    if admin is None:

        cur.execute(
            """
            INSERT INTO users(
                username,
                password,
                role
            )
            VALUES(?,?,?)
            """,
            (
                "admin",
                hash_password("admin123"),
                "Admin"
            )
        )

        conn.commit()

    conn.close()


# =====================================================
# GET USER
# =====================================================

def get_user(username):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cur.fetchone()

    conn.close()

    return user


# =====================================================
# GET ALL USERS
# =====================================================

def get_all_users():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        ORDER BY created_at DESC
        """
    )

    users = cur.fetchall()

    conn.close()

    return users

    # =====================================================
# DELETE USER
# =====================================================

def delete_user(username):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM users
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()
    conn.close()


# =====================================================
# UPDATE ROLE
# =====================================================

def update_role(username, role):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET role=?
        WHERE username=?
        """,
        (
            role,
            username
        )
    )

    conn.commit()
    conn.close()


# =====================================================
# UPDATE PASSWORD
# =====================================================

def update_password(username, new_password):

    hashed = hash_password(new_password)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            hashed,
            username
        )
    )

    conn.commit()
    conn.close()


# =====================================================
# CHANGE PASSWORD
# =====================================================

def change_password(username, old_password, new_password):

    user = get_user(username)

    if user is None:
        return False, "User not found."

    if not verify_password(old_password, user["password"]):
        return False, "Current password is incorrect."

    if len(new_password) < 6:
        return False, "Password must contain at least 6 characters."

    update_password(username, new_password)

    return True, "Password updated successfully."


# =====================================================
# USER EXISTS
# =====================================================

def user_exists(username):

    return get_user(username) is not None


# =====================================================
# RESET PASSWORD (ADMIN)
# =====================================================

def reset_password(username, new_password="123456"):

    if not user_exists(username):
        return False

    update_password(username, new_password)

    return True