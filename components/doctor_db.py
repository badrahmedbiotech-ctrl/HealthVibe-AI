import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================
# DATABASE
# ==========================================

DB_PATH = Path("database")
DB_PATH.mkdir(exist_ok=True)

DATABASE = DB_PATH / "healthvibe.db"


def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# CREATE TABLE
# ==========================================

def create_doctors_table():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctors(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        department TEXT,

        specialization TEXT,

        experience INTEGER,

        available INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()

    # ==========================================
# ADD DOCTOR
# ==========================================

def add_doctor(
    name,
    department,
    specialization,
    experience,
    available
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO doctors(

            name,
            department,
            specialization,
            experience,
            available

        )

        VALUES(?,?,?,?,?)
        """,
        (
            name,
            department,
            specialization,
            experience,
            1 if available else 0
        )
    )

    conn.commit()
    conn.close()


# ==========================================
# GET ALL DOCTORS
# ==========================================

def get_doctors():

    conn = connect()

    df = pd.read_sql(
        """
        SELECT *
        FROM doctors
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df

    # ==========================================
# SEARCH DOCTOR
# ==========================================

def search_doctor(keyword):

    conn = connect()

    df = pd.read_sql(

        """
        SELECT *
        FROM doctors
        WHERE
            name LIKE ?
            OR department LIKE ?
            OR specialization LIKE ?
        ORDER BY id DESC
        """,

        conn,

        params=(
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )

    )

    conn.close()

    return df


# ==========================================
# GET DOCTOR BY ID
# ==========================================

def get_doctor(doctor_id):

    conn = connect()

    df = pd.read_sql(

        """
        SELECT *
        FROM doctors
        WHERE id=?
        """,

        conn,

        params=(doctor_id,)

    )

    conn.close()

    if len(df) == 0:
        return None

    return df.iloc[0]

    # ==========================================
# UPDATE DOCTOR
# ==========================================

def update_doctor(

    doctor_id,
    name,
    department,
    specialization,
    experience,
    available

):

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """

        UPDATE doctors

        SET

            name=?,
            department=?,
            specialization=?,
            experience=?,
            available=?

        WHERE id=?

        """,

        (

            name,
            department,
            specialization,
            experience,
            1 if available else 0,
            doctor_id

        )

    )

    conn.commit()
    conn.close()


# ==========================================
# DELETE DOCTOR
# ==========================================

def delete_doctor(doctor_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """

        DELETE FROM doctors

        WHERE id=?

        """,

        (doctor_id,)

    )

    conn.commit()
    conn.close()

    # ==========================================
# DOCTORS COUNT
# ==========================================

def doctors_count():

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """
        SELECT COUNT(*)
        FROM doctors
        """

    )

    total = cur.fetchone()[0]

    conn.close()

    return total


# ==========================================
# AVAILABLE DOCTORS
# ==========================================

def available_doctors():

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """
        SELECT COUNT(*)
        FROM doctors
        WHERE available=1
        """

    )

    total = cur.fetchone()[0]

    conn.close()

    return total