import mysql.connector
import random

# Re-use your connection credentials
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Raider007!",  # <-- Put your real MySQL password here
    database="incident_tracker"
)
cursor = conn.cursor()

print("Clear old metrics to avoid primary key conflicts...")
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE incidents;")
cursor.execute("TRUNCATE TABLE assets;")
cursor.execute("TRUNCATE TABLE analysts;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# Lists to build realistic data combinations
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
clearances = ["Public Trust", "Secret", "Top Secret"]
criticalities = ["Low", "Medium", "High"]
attack_types = ["Brute Force Attack", "Phishing Link Clicked", "SQL Injection Attempt", "Ransomware Execution", "DDoS Ingress", "Unauthorised SSH Access", "Malware Outbreak", "Data Exfiltration Attempt"]
statuses = ["Investigating", "Contained", "Closed", "Open"]

print("Generating 100 Security Analysts...")
for i in range(1, 101):
    analyst_id = 100 + i
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    clearance = random.choice(clearances)
    
    cursor.execute(
        "INSERT INTO analysts (analyst_id, first_name, last_name, security_clearance) VALUES (%s, %s, %s, %s)",
        (analyst_id, f_name, l_name, clearance)
    )

print("Generating 50 Enterprise Infrastructure Assets...")
for i in range(1, 51):
    asset_id = i
    ip = f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}"
    device_name = f"NET-NODE-{1000 + i}"
    crit = random.choice(criticalities)
    
    cursor.execute(
        "INSERT INTO assets (asset_id, ip_address, device_name, criticality_level) VALUES (%s, %s, %s, %s)",
        (asset_id, ip, device_name, crit)
    )

print("Generating 250 Active Cyber Incidents...")
for i in range(1, 251):
    incident_id = 5000 + i
    attack = random.choice(attack_types)
    status = random.choice(statuses)
    asset_id = random.randint(1, 50)
    analyst_id = random.randint(101, 200)
    
    # We pass 'Low' for severity - remember our database Trigger will 
    # automatically upgrade it to 'Critical' if the asset_id picked has a 'High' criticality!
    cursor.execute(
        "INSERT INTO incidents (incident_id, incident_type, date_detected, severity, status, asset_id, analyst_id) VALUES (%s, %s, CURDATE(), 'Low', %s, %s, %s)",
        (incident_id, attack, status, asset_id, analyst_id)
    )

conn.commit()
cursor.close()
conn.close()
print("Success! 100 analysts, 50 assets, and 250 incidents have been committed cleanly to MySQL.")