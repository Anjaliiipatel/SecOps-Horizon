from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import pooling
import logging

app = Flask(__name__)

# Configure application logging
logging.basicConfig(level=logging.INFO)

# ==========================================
# ADVANCED: ENTERPRISE CONNECTION POOLING
# ==========================================
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="soc_pool",
        pool_size=5,                # Keeps 5 reusable database connections open in memory
        pool_reset_session=True,    # Automatically cleans up user variables between pages
        host="localhost",
        user="root",                # Update if using a different user account
        password="Raider007!",  # <-- Put your real MySQL password here
        database="incident_tracker"
    )
    logging.info("MySQL Connection Pool initialized successfully.")
except mysql.connector.Error as err:
    logging.error(f"Failed to create connection pool: {err}")
    raise

def get_db_connection():
    # Requests an active, pre-established connection from the memory pool
    return db_pool.get_connection()

# ==========================================
# APPLICATION ROUTES
# ==========================================

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Query 1: Fetch the aggregated analyst workload view
        cursor.execute("SELECT * FROM v_analyst_workload_metrics;")
        metrics = cursor.fetchall()
        
        # Query 2: Fetch the raw, chronological history of all incidents
        cursor.execute("SELECT * FROM incidents ORDER BY date_detected DESC;")
        history = cursor.fetchall()
        
    except mysql.connector.Error as err:
        logging.error(f"Database read error: {err}")
        metrics, history = [], []
    finally:
        cursor.close()
        conn.close() # Returns the connection back to the pool instead of destroying it
    
    return render_template('dashboard.html', metrics=metrics, incidents=history)

@app.route('/add_incident', methods=['POST'])
def add_incident():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Securely extract values from the submitted HTML form
    incident_id = request.form['incident_id']
    incident_type = request.form['incident_type']
    asset_id = request.form['asset_id']
    analyst_id = request.form['analyst_id']
    
    # ==========================================
    # SECURITY: STALWART SQL PARAMETERIZATION
    # ==========================================
    # Using %s wildcards completely prevents SQL Injection (SQLi) attacks.
    query = """
    INSERT INTO incidents (incident_id, incident_type, date_detected, severity, status, asset_id, analyst_id)
    VALUES (%s, %s, CURDATE(), 'Low', 'Investigating', %s, %s)
    """
    
    try:
        cursor.execute(query, (incident_id, incident_type, asset_id, analyst_id))
        conn.commit()  # Commits the transaction to the database schema
    except mysql.connector.Error as err:
        logging.error(f"Database write error: {err}")
    finally:
        cursor.close()
        conn.close() # Connection goes back to the pool safely
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)