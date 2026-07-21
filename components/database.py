import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================
# DATABASE CONFIG
# ==========================================

DB_PATH = Path("database")
DB_PATH.mkdir(exist_ok=True)

DATABASE = DB_PATH / "healthvibe.db"


# ==========================================
# CONNECT DATABASE
# ==========================================

def connect():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            age INTEGER NOT NULL,

            gender TEXT NOT NULL,

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
        """
    )

    conn.commit()

    conn.close()

# ==========================================
# SAVE PATIENT
# ==========================================

def save_patient(data):

    required_fields = [

        "name",
        "age",
        "gender",
        "weight",
        "height",
        "pregnancies",
        "glucose",
        "blood_pressure",
        "skin_thickness",
        "insulin",
        "bmi",
        "pedigree",
        "prediction",
        "probability"

    ]

    for field in required_fields:

        if field not in data:

            raise ValueError(f"Missing field: {field}")

    conn = connect()

    cur = conn.cursor()

    try:

        cur.execute(

            """
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

            """,

            (

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

            )

        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(f"Database Error: {e}")

        return False

    finally:

        conn.close()

# ==========================================
# GET HISTORY
# ==========================================

def get_history():

    conn = connect()

    try:

        query = """
        SELECT *
        FROM patients
        ORDER BY created_at DESC
        """

        df = pd.read_sql_query(query, conn)

        return df

    except Exception as e:

        print(f"History Error: {e}")

        return pd.DataFrame()

    finally:

        conn.close()


# ==========================================
# SEARCH PATIENT
# ==========================================

def search_patient(name):

    conn = connect()

    try:

        query = """
        SELECT *
        FROM patients
        WHERE full_name LIKE ?
        ORDER BY created_at DESC
        """

        df = pd.read_sql_query(

            query,

            conn,

            params=(f"%{name.strip()}%",)

        )

        return df

    except Exception as e:

        print(f"Search Error: {e}")

        return pd.DataFrame()

    finally:

        conn.close()

# ==========================================
# DELETE PATIENT
# ==========================================

def delete_patient(patient_id):

    conn = connect()

    cur = conn.cursor()

    try:

        cur.execute(

            """
            DELETE FROM patients
            WHERE id=?
            """,

            (patient_id,)

        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(f"Delete Error: {e}")

        return False

    finally:

        conn.close()


# ==========================================
# GET PATIENT BY ID
# ==========================================

def get_patient(patient_id):

    conn = connect()

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(

        """
        SELECT *
        FROM patients
        WHERE id=?
        """,

        (patient_id,)

    )

    patient = cur.fetchone()

    conn.close()

    return patient


# ==========================================
# TOTAL PATIENTS
# ==========================================

def total_patients():

    conn = connect()

    cur = conn.cursor()

    cur.execute(

        """
        SELECT COUNT(*)
        FROM patients
        """

    )

    total = cur.fetchone()[0]

    conn.close()

    return total


# ==========================================
# CLEAR DATABASE
# ==========================================

def clear_database():

    conn = connect()

    cur = conn.cursor()

    try:

        cur.execute(

            """
            DELETE FROM patients
            """

        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(f"Clear Database Error: {e}")

        return False

    finally:

        conn.close()