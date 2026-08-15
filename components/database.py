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

    # ======================================
    # USERS
    # ======================================

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

    # ======================================
    # PATIENT PROFILE
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_profiles(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        full_name TEXT,
        age INTEGER,
        gender TEXT,

        weight REAL,
        height REAL,

        phone TEXT,
        address TEXT,
        birth_date TEXT,
        blood_group TEXT,

        smoking TEXT,
        alcohol TEXT,

        allergies TEXT,
        chronic_diseases TEXT,
        medications TEXT,

        emergency_name TEXT,
        emergency_phone TEXT,
        emergency_relation TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    # ======================================
    # ASSESSMENTS
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assessments(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        disease TEXT,

        prediction TEXT,

        probability REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    # ======================================
    # DIABETES
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS diabetes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        pregnancies INTEGER,

        glucose REAL,

        blood_pressure REAL,

        skin_thickness REAL,

        insulin REAL,

        bmi REAL,

        pedigree REAL,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

    )
    """)

    # ======================================
    # HYPERTENSION
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hypertension(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        systolic REAL,

        diastolic REAL,

        cholesterol REAL,

        heart_rate REAL,

        smoking TEXT,

        activity TEXT,

        salt TEXT,

        alcohol TEXT,

        stress TEXT,

        sleep TEXT,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

    )
    """)

    # ======================================
    # LIPID
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lipid(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        total_cholesterol REAL,

        ldl REAL,

        hdl REAL,

        triglycerides REAL,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

    )
    """)

    # ======================================
    # OBESITY
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS obesity(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        bmi REAL,

        waist REAL,

        activity TEXT,

        calories REAL,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

    )
    """)

    # ======================================
    # FIBROSIS
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fibrosis(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        oxygen REAL,

        fev1 REAL,

        fvc REAL,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

    )
    """)

    # ======================================
    # THROMBOSIS
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS thrombosis(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        assessment_id INTEGER,

        d_dimer REAL,

        platelets REAL,

        inr REAL,

        prediction TEXT,

        FOREIGN KEY(assessment_id)
        REFERENCES assessments(id)

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

    """, (

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
# GET ALL PATIENT PROFILES
# ==========================================

def get_all_profiles():

    conn = connect()

    query = """
        SELECT
            patient_profiles.id,
            patient_profiles.user_id,
            patient_profiles.full_name AS name,
            users.email,
            patient_profiles.gender,
            patient_profiles.age,
            patient_profiles.created_at

        FROM patient_profiles

        LEFT JOIN users
            ON patient_profiles.user_id = users.id

        ORDER BY datetime(patient_profiles.created_at) DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

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
# SAVE ASSESSMENT
# ==========================================

def save_assessment(
    user_id,
    disease,
    prediction,
    probability
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO assessments(

        user_id,
        disease,
        prediction,
        probability

    )

    VALUES(?,?,?,?)

    """,(

        user_id,
        disease,
        prediction,
        probability

    ))

    conn.commit()

    assessment_id = cur.lastrowid

    conn.close()

    return assessment_id

# ==========================================
# GET PATIENT HISTORY
# ==========================================

def get_patient_history(user_id):

    conn = connect()

    query = """
    SELECT *
    FROM assessments
    WHERE user_id = ?
    ORDER BY created_at DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    conn.close()

    return df

# ==========================================
# SAVE DIABETES
# ==========================================

def save_diabetes(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO diabetes(

        assessment_id,

        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        pedigree,

        prediction

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("pregnancies",0),
        patient.get("glucose",0),
        patient.get("blood_pressure",0),
        patient.get("skin", 0),
        patient.get("insulin",0),
        patient.get("bmi",0),
        patient.get("dpf", 0),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE HYPERTENSION
# ==========================================

def save_hypertension(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO hypertension(

        assessment_id,

        systolic,
        diastolic,
        cholesterol,
        heart_rate,

        smoking,
        activity,
        salt,
        alcohol,

        stress,
        sleep,

        prediction

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("systolic",120),
        patient.get("diastolic",80),
        patient.get("cholesterol",200),
        patient.get("heart_rate",75),

        patient.get("smoking","No"),
        patient.get("activity",""),
        patient.get("salt",""),
        patient.get("alcohol",""),

        patient.get("stress",""),
        patient.get("sleep",""),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE LIPID
# ==========================================

def save_lipid(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO lipid(

        assessment_id,

        total_cholesterol,
        ldl,
        hdl,
        triglycerides,

        prediction

    )

    VALUES(?,?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("total_cholesterol",0),
        patient.get("ldl",0),
        patient.get("hdl",0),
        patient.get("triglycerides",0),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()

# ==========================================
# SAVE OBESITY
# ==========================================

def save_obesity(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO obesity(

        assessment_id,

        bmi,
        waist,
        activity,
        calories,

        prediction

    )

    VALUES(?,?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("bmi",0),
        patient.get("waist",0),
        patient.get("activity",""),
        patient.get("calories",0),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE FIBROSIS
# ==========================================

def save_fibrosis(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO fibrosis(

        assessment_id,

        oxygen,
        fev1,
        fvc,

        prediction

    )

    VALUES(?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("oxygen",0),
        patient.get("fev1",0),
        patient.get("fvc",0),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE THROMBOSIS
# ==========================================

def save_thrombosis(
    assessment_id,
    patient
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO thrombosis(

        assessment_id,

        d_dimer,
        platelets,
        inr,

        prediction

    )

    VALUES(?,?,?,?,?)

    """,(

        assessment_id,

        patient.get("d_dimer",0),
        patient.get("platelets",0),
        patient.get("inr",0),

        str(patient.get("prediction",""))

    ))

    conn.commit()
    conn.close()


# ==========================================
# USER HISTORY
# ==========================================

def get_user_history(user_id):

    conn = connect()

    df = pd.read_sql_query("""

        SELECT *

        FROM assessments

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

    query = """
        SELECT
            assessments.id,
            assessments.user_id,
            users.full_name AS patient_name,
            assessments.disease,
            assessments.prediction,
            assessments.probability,
            assessments.created_at

        FROM assessments

        LEFT JOIN users
            ON assessments.user_id = users.id

        ORDER BY datetime(assessments.created_at) DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# ==========================================
# TOTAL ASSESSMENTS
# ==========================================

def total_patients():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='Patient'"
    )

    total = cur.fetchone()[0]

    conn.close()

    return total

# ==========================================
# DELETE HISTORY
# ==========================================

def delete_history(history_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM assessments WHERE id = ?",
        (history_id,)
    )

    conn.commit()
    conn.close()

# ==========================================
# TOTAL ASSESSMENTS
# ==========================================

def total_assessments():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM assessments")

    total = cur.fetchone()[0]

    conn.close()

    return total
# ==========================================
# DELETE ALL HISTORY FOR USER
# ==========================================

def delete_all_history(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM assessments WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def get_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user

# ==========================================
# UPDATE USER NAME
# ==========================================

def update_user_name(user_id, full_name):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET full_name=?
        WHERE id=?
        """,
        (full_name, user_id)
    )

    conn.commit()
    conn.close()

# ==========================================
# DELETE USER
# ==========================================

def delete_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()
# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def average_risk(user_id=None):
    """
    Calculate average assessment probability.
    Returns 0 if there are no assessments.
    """

    conn = connect()

    if user_id is not None:

        query = """
        SELECT AVG(probability)
        FROM assessments
        WHERE user_id = ?
        """

        result = conn.execute(
            query,
            (user_id,)
        ).fetchone()[0]

    else:

        query = """
        SELECT AVG(probability)
        FROM assessments
        """

        result = conn.execute(query).fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return float(result)


def latest_assessments(limit=5, user_id=None):
    """
    Return latest assessments as a DataFrame.
    """

    conn = connect()

    if user_id is not None:

        query = """
        SELECT *
        FROM assessments
        WHERE user_id = ?
        ORDER BY datetime(created_at) DESC
        LIMIT ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(user_id, limit)
        )

    else:

        query = """
        SELECT *
        FROM assessments
        ORDER BY datetime(created_at) DESC
        LIMIT ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(limit,)
        )

    conn.close()

    return df


def disease_statistics(user_id=None):
    """
    Return assessment count grouped by disease.
    """

    conn = connect()

    if user_id is not None:

        query = """
        SELECT
            disease,
            COUNT(*) AS count
        FROM assessments
        WHERE user_id = ?
        GROUP BY disease
        ORDER BY count DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(user_id,)
        )

    else:

        query = """
        SELECT
            disease,
            COUNT(*) AS count
        FROM assessments
        GROUP BY disease
        ORDER BY count DESC
        """

        df = pd.read_sql_query(
            query,
            conn
        )

    conn.close()

    return df


def risk_statistics(user_id=None):

    conn = connect()

    if user_id is not None:

        query = """
            SELECT
                disease AS Disease,
                ROUND(AVG(probability), 2) AS "Average Risk"

            FROM assessments

            WHERE user_id = ?

            GROUP BY disease

            ORDER BY "Average Risk" DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(user_id,)
        )

    else:

        query = """
            SELECT
                disease AS Disease,
                ROUND(AVG(probability), 2) AS "Average Risk"

            FROM assessments

            GROUP BY disease

            ORDER BY "Average Risk" DESC
        """

        df = pd.read_sql_query(
            query,
            conn
        )

    conn.close()

    return df