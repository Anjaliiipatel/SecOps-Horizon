from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",                     # Change to your MySQL user if different
        password="Raider007!", # <-- Put your real MySQL password here
        database="incident_tracker"
    )

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query 1: Fetch the aggregated analyst workload view
    cursor.execute("SELECT * FROM v_analyst_workload_metrics;")
    metrics = cursor.fetchall()
    
    # Query 2: Fetch the raw, chronological history of all incidents
    cursor.execute("SELECT * FROM incidents ORDER BY date_detected DESC;")
    history = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Pass both datasets to the frontend template
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
    
    # Parameterized Query prevents SQL Injection vulnerabilities
    query = """
    INSERT INTO incidents (incident_id, incident_type, date_detected, severity, status, asset_id, analyst_id)
    VALUES (%s, %s, CURDATE(), 'Low', 'Investigating', %s, %s)
    """
    
    cursor.execute(query, (incident_id, incident_type, asset_id, analyst_id))
    conn.commit()  # Saves the changes to the database
    
    cursor.close()
    conn.close()
    
    # Redirect back to the home page to display the freshly added incident
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)