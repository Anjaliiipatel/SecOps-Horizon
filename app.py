from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import pooling
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="soc_pool",
        pool_size=5,
        pool_reset_session=True,
        host="localhost",
        user="root",
        password="Raider007!",  # <-- Put your real MySQL password here
        database="incident_tracker"
    )
except mysql.connector.Error as err:
    logging.error(f"Pool creation failure: {err}")
    raise

def get_db_connection():
    return db_pool.get_connection()

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Query 1: Fetch aggregated analyst workload metrics
        cursor.execute("SELECT * FROM v_analyst_workload_metrics;")
        metrics = cursor.fetchall()
        
        # Query 2: Fetch chronological incident history logs
        cursor.execute("SELECT * FROM incidents ORDER BY date_detected DESC LIMIT 50;")
        history = cursor.fetchall()
        
        # Query 3: Fetch structural graph metrics counting types of active threats
        cursor.execute("""
            SELECT incident_type, COUNT(*) as volume 
            FROM incidents 
            GROUP BY incident_type;
        """)
        chart_data = cursor.fetchall()
        
    except mysql.connector.Error as err:
        logging.error(f"Read failure: {err}")
        metrics, history, chart_data = [], [], []
    finally:
        cursor.close()
        conn.close()
    
    return render_template('dashboard.html', metrics=metrics, incidents=history, chart_data=chart_data)

@app.route('/add_incident', methods=['POST'])
def add_incident():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO incidents (incident_id, incident_type, date_detected, severity, status, asset_id, analyst_id)
    VALUES (%s, %s, CURDATE(), 'Low', 'Investigating', %s, %s)
    """
    try:
        cursor.execute(query, (request.form['incident_id'], request.form['incident_type'], request.form['asset_id'], request.form['analyst_id']))
        conn.commit()
    except mysql.connector.Error as err:
        logging.error(f"Write failure: {err}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)