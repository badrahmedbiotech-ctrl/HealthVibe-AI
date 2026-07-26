import sqlite3
import pandas as pd


DB_NAME = "database/healthvibe.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(

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


def insert_patient(data):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

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

    """, data)

    conn.commit()

    conn.close()


def get_all_patients():

    conn = connect()

    df = pd.read_sql_query(

        "SELECT * FROM patients ORDER BY id DESC",

        conn

    )

    conn.close()

    return df