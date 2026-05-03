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
        last_used DATETIME,
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT NOT NULL,
        total_quantity INTEGER,
        available_quantity INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        package_id INTEGER,
        purchased_count INTEGER,
        FOREIGN KEY (package_id) REFERENCES packages(id)
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

    # Seed rentals
    rentals = [
        ("Notebook (High Performance)", 10, 3),
        ("Projector", 5, 5),
        ("Virtual Machine (Standard)", 50, 12),
        ("Testing Phone (iOS)", 8, 2)
    ]
    cursor.executemany("INSERT OR IGNORE INTO rentals (asset_type, total_quantity, available_quantity) VALUES (?, ?, ?)", rentals)

    # Seed licenses
    licenses = [
        (1, 100), # Adobe Acrobat: 100 licenses
        (2, 500), # Chrome: 500 licenses
        (3, 10),  # Neo42 Agent: 10 licenses (will show near limit)
        (4, 50)   # Teams: 50 licenses
    ]
    cursor.executemany("INSERT OR IGNORE INTO licenses (package_id, purchased_count) VALUES (?, ?)", licenses)

    # Seed deployments (PackageID, EndpointID, Status, LastUsed, ErrorLog)
    deployments = [
        (1, 1, "Success", "2026-05-01", None),
        (2, 1, "Success", "2026-04-15", None),
        (3, 1, "Failed", None, "Error: 0x80070005 - Access Denied"),
        (1, 2, "Success", "2026-02-01", None), # Old usage! Reclaimable
        (4, 2, "Success", "2026-01-10", None), # Old usage! Reclaimable
        (3, 3, "In Progress", None, None)
    ]
    cursor.executemany("INSERT INTO deployments (package_id, endpoint_id, status, last_used, error_log) VALUES (?, ?, ?, ?, ?)", deployments)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
