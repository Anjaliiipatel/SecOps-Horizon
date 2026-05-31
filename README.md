# SecOps Horizon — Automated Cyber Threat Analytics Engine 🛡️

SecOps Horizon is a high-fidelity, data-driven Security Operations Center (SOC) dashboard. The application bridges full-stack engineering with infrastructure security by wiring a **Python Flask** application engine directly to a hardened **MySQL** relational database backend. 

Featuring custom database automation, optimized collection pooling, and a premium iOS-style user interface, the platform visualizes multi-series telemetry vectors using real-time animated line graphs via **Chart.js**.

---

## 🚀 Key Architectural Features

* **Database-Level Automation:** Configured active **SQL Triggers** that intercept rows before execution to automatically escalate incident threat levels based on targeted asset criticality.
* **Optimized Data Aggregation:** Structured analytical **Database Views** to query, calculate, and consolidate real-time workload parameters across 100 active security responders simultaneously.
* **Stalwart Application Security:** Enforced strict **SQL Parameterization (Prepared Statements)** across all data-entry forms to completely neutralize SQL Injection (SQLi) attack vectors.
* **Enterprise Connection Pooling:** Integrated a server-side `MySQLConnectionPool` object to maintain persistent caches of reusable connections, preventing server failure under heavy concurrent traffic.
* **Asynchronous Telemetry Stream:** Utilized native JavaScript streaming loops over a **Tailwind CSS** framework to render smooth micro-animations and interactive data line graphs.

---

## 📂 System Directory Structure

```text
cyber-dashboard/
│
├── app.py                  # Python Flask backend (Connection Pool Gateway)
├── requirements.txt        # System module dependencies listing
├── seed_data.py            # Utility automation script (populates 100 mock profiles)
└── templates/
    └── dashboard.html      # Premium iOS-style UI Layout with Chart.js Engine
