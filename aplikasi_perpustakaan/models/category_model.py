import sqlite3
import os

# Use database in temp directory to avoid file locking issues
DB_DIR = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp', 'perpustakaan_app')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'app.db')

def get_connection():
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_category(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()

def get_all_categories():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM categories")
    rows = c.fetchall()
    conn.close()
    return rows

def update_category(category_id, name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE categories SET name=? WHERE id=?",
        (name, category_id)
    )
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "DELETE FROM categories WHERE id=?",
        (category_id,)
    )
    conn.commit()
    conn.close()
