-- Create the main database schema
CREATE DATABASE IF NOT EXISTS incident_tracker;
USE incident_tracker;

-- Drop existing structures if running this setup script again
DROP VIEW IF EXISTS v_analyst_workload_metrics;
DROP TRIGGER IF EXISTS escalate_critical_assets;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS analysts;

-- Table 1: Assets Registry
CREATE TABLE assets (
    asset_id INT PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    device_name VARCHAR(100) NOT NULL,
    criticality_level VARCHAR(45) NOT NULL
);

-- Table 2: Security Analysts Roster
CREATE TABLE analysts (
    analyst_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    security_clearance VARCHAR(45) NOT NULL
);

-- Table 3: Incidents Log (with Foreign Key Links)
CREATE TABLE incidents (
    incident_id INT PRIMARY KEY,
    incident_type VARCHAR(100) NOT NULL,
    date_detected DATE NOT NULL,
    severity VARCHAR(45) NOT NULL,
    status VARCHAR(45) NOT NULL,
    asset_id INT,
    analyst_id INT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE SET NULL,
    FOREIGN KEY (analyst_id) REFERENCES analysts(analyst_id) ON DELETE SET NULL
);

-- Automation Trigger: Auto-escalate attacks hitting critical infrastructure
DELIMITER $$
CREATE TRIGGER escalate_critical_assets
BEFORE INSERT ON incidents
FOR EACH ROW
BEGIN
    DECLARE asset_crit VARCHAR(50);
    
    SELECT criticality_level INTO asset_crit 
    FROM assets 
    WHERE asset_id = NEW.asset_id;
    
    IF asset_crit = 'High' THEN
        SET NEW.severity = 'Critical';
    END IF;
END$$
DELIMITER ;

-- Live Dashboard View: Aggregates statistics for individual analysts
CREATE VIEW v_analyst_workload_metrics AS
SELECT 
    CONCAT(a.first_name, ' ', a.last_name) AS analyst_name,
    COUNT(i.incident_id) AS total_assigned_incidents,
    SUM(CASE WHEN i.status != 'Contained' AND i.status != 'Closed' THEN 1 ELSE 0 END) AS active_threats,
    SUM(CASE WHEN i.severity = 'Critical' THEN 1 ELSE 0 END) AS handling_critical_threats
FROM analysts a
LEFT JOIN incidents i ON a.analyst_id = i.analyst_id
GROUP BY a.analyst_id, a.first_name, a.last_name;

-- Seed Data: Baseline information to populate your interface immediately
INSERT INTO assets VALUES (1, '10.0.0.45', 'DC-01-PROD', 'High');
INSERT INTO assets VALUES (2, '10.0.0.112', 'WKSTN-HR-04', 'Low');
INSERT INTO assets VALUES (3, '192.168.1.20', 'AWS-WEB-SRV01', 'Medium');

INSERT INTO analysts VALUES (101, 'Alex', 'Rodriguez', 'Secret');
INSERT INTO analysts VALUES (102, 'Sarah', 'Chen', 'Top Secret');
INSERT INTO analysts VALUES (103, 'Marcus', 'Vance', 'Public Trust');

INSERT INTO incidents VALUES (1001, 'Brute Force Attack', '2026-05-28', 'Medium', 'Investigating', 1, 102);
INSERT INTO incidents VALUES (1002, 'Phishing Link Clicked', '2026-05-29', 'Low', 'Contained', 2, 101);
INSERT INTO incidents VALUES (1003, 'SQL Injection Attempt', '2026-05-30', 'Medium', 'Closed', 3, 103);
 -- 1. Expand the Analyst Roster with varied tiers and clearances
INSERT INTO analysts (analyst_id, first_name, last_name, security_clearance) VALUES
(104, 'David', 'Kim', 'Secret'),
(105, 'Elena', 'Rostova', 'Top Secret'),
(106, 'Jamal', 'Washington', 'Public Trust'),
(107, 'Chloe', 'Bourgeois', 'Secret');

-- 2. Expand the Assets Registry with critical infrastructure and endpoints
INSERT INTO assets (asset_id, ip_address, device_name, criticality_level) VALUES
(4, '10.0.1.10', 'SQL-PROD-DB01', 'High'),      -- Production Database Server
(5, '10.0.5.22', 'VPN-GATEWAY', 'High'),        -- Corporate VPN Access Point
(6, '192.168.2.50', 'DEV-LEADER-LAP', 'Medium'), -- Engineering Team Laptop
(7, '172.16.0.4', 'RECEPTION-DESK', 'Low');     -- Front Desk Kiosk

-- 3. Log a fresh wave of realistic cyber threats 
-- (Notice how hitting Asset 4 or 5 will fire your background trigger automatically!)
INSERT INTO incidents (incident_id, incident_type, date_detected, severity, status, asset_id, analyst_id) VALUES
(1008, 'DDoS Attack Attempt', '2026-05-31', 'Medium', 'Investigating', 5, 105), -- Target: VPN (High) -> Auto-escalates to Critical!
(1009, 'Malware Outbreak', '2026-05-31', 'Low', 'Investigating', 7, 104),     -- Target: Reception (Low)
(1010, 'Privilege Escalation', '2026-05-31', 'High', 'Open', 4, 102),          -- Target: Prod DB (High) -> Auto-escalates to Critical!
(1011, 'Unauthorized USB Ingress', '2026-05-31', 'Low', 'Contained', 6, 106),  -- Target: Dev Laptop (Medium)
(1012, 'Suspicious SSH Login', '2026-05-31', 'Low', 'Closed', 1, 107);         -- Target: Domain Controller (High) -> Auto-escalates!
