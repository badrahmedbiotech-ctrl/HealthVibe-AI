import sqlite3
from pathlib import Path
import pandas as pd
import hashlib

# ==========================================
# DATABASE
# ==========================================

DB_FOLDER = Path("database")
DB_FOLDER.mkdir(exist_ok=True)

DATABASE = DB_FOLDER / "healthvibe.db"


# ==========================================
# CONNECT
# ==========================================

def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    conn = connect()
    cur = conn.cursor()

    # ---------------- USERS ----------------

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


    # ---------------- PATIENTS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS patient_profiles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

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

    prediction TEXT,
    probability REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id) REFERENCES users(id)

)

""")
    conn.commit()
    conn.close()


create_tables()


# ==========================================
# REGISTER
# ==========================================

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

        """,(

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


# ==========================================
# LOGIN
# ==========================================

def login_user(email, password):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM users

    WHERE email=?
    AND password=?

    """,(

        email,
        hash_password(password)

    ))

    user = cur.fetchone()

    conn.close()

    return user

# ==========================================
# CREATE PROFILE
# ==========================================

def create_profile(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT OR IGNORE INTO patient_profiles(

        user_id

    )

    VALUES(?)

    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================================
# GET PROFILE
# ==========================================

def get_profile(user_id):

    conn = connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM patient_profiles

    WHERE user_id=?

    """, (user_id,))

    profile = cur.fetchone()

    conn.close()

    return profile


# ==========================================
# UPDATE PROFILE
# ==========================================

def update_profile(data):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    UPDATE patient_profiles

    SET

        full_name=?,
        age=?,
        gender=?,
        weight=?,
        height=?,

        phone=?,
        address=?,
        birth_date=?,
        blood_group=?,

        smoking=?,
        alcohol=?,

        allergies=?,
        chronic_diseases=?,
        medications=?,

        emergency_name=?,
        emergency_phone=?,
        emergency_relation=?

    WHERE user_id=?

    """, (

        data["full_name"],
        data["age"],
        data["gender"],
        data["weight"],
        data["height"],

        data["phone"],
        data["address"],
        data["birth_date"],
        data["blood_group"],

        data["smoking"],
        data["alcohol"],

        data["allergies"],
        data["chronic_diseases"],
        data["medications"],

        data["emergency_name"],
        data["emergency_phone"],
        data["emergency_relation"],

        data["user_id"]

    ))

    conn.commit()
    conn.close()

# ==========================================
# SAVE PATIENT HISTORY
# ==========================================

def save_patient(data):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO patients(

        user_id,
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

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

        data["user_id"],
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
# USER HISTORY
# ==========================================

def get_user_history(user_id):

    conn = connect()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM patients

        WHERE user_id=?

        ORDER BY created_at DESC

        """,

        conn,

        params=(user_id,)

    )

    conn.close()

    return df


# ==========================================
# ALL HISTORY
# ==========================================

def get_all_history():

    conn = connect()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM patients

        ORDER BY created_at DESC

        """,

        conn

    )

    conn.close()

    return df


# ==========================================
# TOTAL PATIENTS
# ==========================================

def total_patients():

    conn = connect()
    cur = conn.cursor()

    cur.execute(

        "SELECT COUNT(*) FROM patients"

    )

    total = cur.fetchone()[0]

    conn.close()

    return total