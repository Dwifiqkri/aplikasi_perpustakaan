import sqlite3
import os

# Use same path as models
models_dir = os.path.dirname(__file__)
DB_PATH = os.path.normpath(os.path.join(models_dir, 'models', '..', 'database', 'app.db'))

print(f"Connecting to: {DB_PATH}")
print(f"File exists: {os.path.exists(DB_PATH)}")

try:
    conn = sqlite3.connect(DB_PATH, timeout=5)
    c = conn.cursor()
    
    # Check existing tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"Tables: {tables}")
    
    # Delete all data
    for table in tables:
        table_name = table[0]
        if table_name != 'sqlite_sequence':
            c.execute(f"DELETE FROM {table_name}")
            print(f"✓ Cleared table: {table_name}")
    
    # Reset auto-increment
    c.execute("DELETE FROM sqlite_sequence")
    print("✓ Reset auto-increment")
    
    conn.commit()
    conn.close()
    
    print("\n✓ Database berhasil di-kosongkan!")
    
except sqlite3.Error as e:
    print(f"✗ Error: {e}")
