from flask import Flask, render_template
try:
    import mysql.connector as mysql_connector  # type: ignore[reportMissingImports]
except Exception:
    # Import may fail in some linting/analysis environments where
    # the mysql-connector-python package is not installed. Defer
    # raising until runtime so editors don't always error out.
    mysql_connector = None

app = Flask(__name__)

def get_db_connection():
    if mysql_connector is None:
        raise RuntimeError(
            "mysql.connector is not available. Install with: pip install mysql-connector-python"
        )
    return mysql_connector.connect(
        host="localhost",
        user="root",                     # You can change to 'tier1_analyst' if configured
        password="Raider007!", # <-- Update with your real database password
        database="incident_tracker"
    )

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query data directly out of the live dashboard analytics view
    cursor.execute("SELECT * FROM v_analyst_workload_metrics;")
    metrics = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('dashboard.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5000)