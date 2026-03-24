import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "pqc_framework")
    )


def save_scan(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO scans (
            domain,
            algorithm,
            key_size,
            tls_version,
            cipher_suite,
            signature_algorithm,
            category,
            usage_type,
            quantum_threat,
            impact,
            risk_level,
            risk_score,
            recommended_path,
            next_step,
            final_goal
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.get("domain"),
        data.get("algorithm"),
        str(data.get("key_size")),
        data.get("tls_version"),
        data.get("cipher_suite"),
        data.get("signature_algorithm"),
        data.get("category"),
        data.get("usage"),
        data.get("quantum_threat"),
        data.get("impact"),
        data.get("risk_level"),
        data.get("risk_score"),
        data.get("recommended_path"),
        data.get("next_step"),
        data.get("final_goal")
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

def get_all_scans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM scans ORDER BY scanned_at DESC")
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records

def get_total_scans():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def get_risk_distribution():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT risk_level, COUNT(*) as count
        FROM scans
        GROUP BY risk_level
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_algorithm_distribution():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT algorithm, COUNT(*) as count
        FROM scans
        GROUP BY algorithm
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_scan_by_id(scan_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM scans WHERE id = %s", (scan_id,))
    record = cursor.fetchone()

    cursor.close()
    conn.close()

    return record