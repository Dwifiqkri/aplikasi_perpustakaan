import os
import sqlite3
import shutil

# Database path
DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')

# Backup old database if exists
backup_path = os.path.join(DB_DIR, 'app.db.backup')
if os.path.exists(DB_PATH):
    try:
        shutil.copy2(DB_PATH, backup_path)
        os.remove(DB_PATH)
        print(f"✓ Database lama di-backup ke: {backup_path}")
        print(f"✓ File lama dihapus")
    except Exception as e:
        print(f"✗ Gagal menghapus database lama: {e}")

# Ensure directory exists
os.makedirs(DB_DIR, exist_ok=True)

# Create new database with tables
try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create books table
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            stock INTEGER,
            image_path TEXT
        )
    """)
    print("✓ Tabel books berhasil dibuat")
    
    # Create categories table
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    print("✓ Tabel categories berhasil dibuat")
    
    # Create users table (jika diperlukan)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT
        )
    """)
    print("✓ Tabel users berhasil dibuat")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Database baru berhasil dibuat di: {DB_PATH}")
    
except sqlite3.Error as e:
    print(f"✗ Error membuat database: {e}")
    exit(1)
