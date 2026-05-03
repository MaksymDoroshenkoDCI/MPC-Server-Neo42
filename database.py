import sqlite3
import os

DB_PATH = "neo42_apc.db"

def init_db():
    """Initializes the mock Neo42 Application Package Center database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        category TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS endpoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT NOT NULL UNIQUE,
        os TEXT,
        ip_address TEXT,
        location TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deployments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        package_id INTEGER,
        endpoint_id INTEGER,
        status TEXT,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        error_log TEXT,
        FOREIGN KEY (package_id) REFERENCES packages(id),
        FOREIGN KEY (endpoint_id) REFERENCES endpoints(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pipelines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT,
        current_step TEXT,
        progress INTEGER,
        FOREIGN KEY (id) REFERENCES deployments(id)
    )
    ''')

    # Seed data
    packages = [
        ("Adobe Acrobat Reader", "2024.001", "Office"),
        ("Google Chrome", "124.0.6367", "Browser"),
        ("Neo42 Service Agent", "4.2.0", "System"),
        ("Microsoft Teams", "24091.214", "Communication"),
        ("Visual Studio Code", "1.88.0", "Development")
    ]
    cursor.executemany("INSERT OR IGNORE INTO packages (name, version, category) VALUES (?, ?, ?)", packages)

    endpoints = [
        ("SRV-PROD-01", "Windows Server 2022", "10.0.0.10", "Berlin"),
        ("SRV-PROD-02", "Windows Server 2022", "10.0.0.11", "Frankfurt"),
        ("WS-DEV-MAX", "Windows 11", "192.168.1.45", "Remote"),
        ("WS-SUP-01", "Windows 10", "10.0.2.5", "Berlin")
    ]
    cursor.executemany("INSERT OR IGNORE INTO endpoints (hostname, os, ip_address, location) VALUES (?, ?, ?, ?)", endpoints)

    # Seed deployments
    deployments = [
        (1, 1, "Success", None),
        (2, 1, "Success", None),
        (3, 1, "Failed", "Error: 0x80070005 - Access Denied"),
        (1, 2, "Success", None),
        (3, 3, "In Progress", None)
    ]
    cursor.executemany("INSERT INTO deployments (package_id, endpoint_id, status, error_log) VALUES (?, ?, ?, ?)", deployments)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
