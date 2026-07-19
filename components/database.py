import sqlite3
from pathlib import Path
import pandas as pd


DB_PATH = Path("database")
DB_PATH.mkdir(exist_ok=True)

DATABASE = DB_PATH / "healthvibe.db"


# ==========================================
# CONNECT
# ==========================================

def connect():
    return sqlite3.connect(DATABASE)


# ==========================================
# CREATE TABLE
# ==========================================

def create_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT,

        age INTEGER,

        gender TEXT,

        weight REAL,

        height REAL,

        pregnancies INTEGER,

        glucose REAL,

        blood_pressure REAL,

        skin_thickness REAL,

        insulin REAL,

        bmi REAL,

        pedigree REAL,

        prediction INTEGER,

        probability REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SAVE PATIENT
# ==========================================

def save_patient(data):

    conn = connect()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO patients(

        full_name,
        age,
        gender,
        weight,
        height,
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        pedigree,
        prediction,
        probability

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

        data["name"],
        data["age"],
        data["gender"],
        data["weight"],
        data["height"],
        data["pregnancies"],
        data["glucose"],
        data["blood_pressure"],
        data["skin_thickness"],
        data["insulin"],
        data["bmi"],
        data["pedigree"],
        data["prediction"],
        data["probability"]

    ))

    conn.commit()
    conn.close()


# ==========================================
# GET HISTORY
# ==========================================

def get_history():

    conn = connect()

    df = pd.read_sql(

        """
        SELECT *
        FROM patients
        ORDER BY id DESC
        """,

        conn

    )

    conn.close()

    return df


# ==========================================
# SEARCH
# ==========================================

def search_patient(name):

    conn = connect()

    df = pd.read_sql(

        """
        SELECT *
        FROM patients
        WHERE full_name LIKE ?
        ORDER BY id DESC
        """,

        conn,

        params=(f"%{name}%",)

    )

    conn.close()

    return df

# ==========================================
# DELETE PATIENT
# ==========================================

def delete_patient(patient_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()