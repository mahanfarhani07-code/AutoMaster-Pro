import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("automaster.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT,
                model TEXT,
                year INTEGER,
                color TEXT,
                plate TEXT,
                owner_id INTEGER,
                image_path TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES customers(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                mechanic_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                cost REAL NOT NULL DEFAULT 0,
                service_date TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS mechanics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                specialty TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                part_number TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                price REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                car_id INTEGER,
                total REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'unpaid',
                invoice_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
                FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE SET NULL
            );

            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('admin', 'admin123', 'admin');
            """
        )


def dashboard_counts():
    with get_connection() as conn:
        return {
            "cars": conn.execute("SELECT COUNT(*) FROM cars").fetchone()[0],
            "customers": conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0],
            "services": conn.execute("SELECT COUNT(*) FROM services").fetchone()[0],
            "income": conn.execute("SELECT COALESCE(SUM(total), 0) FROM invoices WHERE status = 'paid'").fetchone()[0],
        }
