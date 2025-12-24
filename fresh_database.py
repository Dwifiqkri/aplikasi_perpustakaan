import sqlite3
import os
import shutil

DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')

# Create in a temp location first
TEMP_DB = os.path.join(DB_DIR, 'app_new.db')

print(f"Creating database in temp location: {TEMP_DB}")

try:
    # Create fresh database in temp location
    conn = sqlite3.connect(TEMP_DB)
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
    print("✓ Created books table")
    
    # Create categories table
    c.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    print("✓ Created categories table")
    
    # Create users table
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
    
    print(f"✓ Temp database created successfully")
    
    # Now try to replace the old one
    try:
        # Remove old database
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"✓ Removed old database")
    except:
        print("⚠ Could not remove old database, will overwrite")
    
    # Move temp to main
    shutil.move(TEMP_DB, DB_PATH)
    print(f"\n✓ Database replacement successful!")
    print(f"  Lokasi: {DB_PATH}")
    print(f"  Status: FRESH & EMPTY")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
