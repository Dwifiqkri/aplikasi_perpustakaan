import sqlite3
import os
import time

DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')

# Try to close any existing connections by importing and resetting
try:
    import sys
    # Remove cached modules
    if 'models.book_model' in sys.modules:
        del sys.modules['models.book_model']
    if 'models.category_model' in sys.modules:
        del sys.modules['models.category_model']
    print("✓ Cleared module cache")
except:
    pass

# Wait a moment for connections to close
time.sleep(1)

# Try to create a fresh database
os.makedirs(DB_DIR, exist_ok=True)

try:
    # Remove old one if we can
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"✓ Deleted old database")
        except Exception as e:
            print(f"⚠ Could not delete old database: {e}")
            print("Creating new connection...")
    
    # Create new database
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    
    # Create books table
    c.execute("DROP TABLE IF EXISTS books")
    c.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            stock INTEGER,
            image_path TEXT
        )
    """)
    print("✓ Created books table")
    
    # Create categories table
    c.execute("DROP TABLE IF EXISTS categories")
    c.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    print("✓ Created categories table")
    
    # Create users table
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT
        )
    """)
    print("✓ Created users table")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Database baru berhasil dibuat (KOSONG)")
    print(f"  Lokasi: {DB_PATH}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
