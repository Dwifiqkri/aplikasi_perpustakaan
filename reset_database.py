import os
import sqlite3

# Database path
DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')

# Reset database - delete and recreate
try:
    # Remove old database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Database lama dihapus")
    
    # Ensure directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Create new database with tables
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create books table
    c.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            stock INTEGER,
            image_path TEXT
        )
    """)
    print("✓ Tabel books berhasil dibuat (kosong)")
    
    # Create categories table
    c.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    print("✓ Tabel categories berhasil dibuat (kosong)")
    
    # Create users table
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT
        )
    """)
    print("✓ Tabel users berhasil dibuat (kosong)")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Database baru (KOSONG) berhasil dibuat!")
    print(f"  Lokasi: {DB_PATH}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
