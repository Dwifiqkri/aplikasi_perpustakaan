import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'app.db')

print(f"Clearing database: {DB_PATH}")

try:
    # Open with longer timeout
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.isolation_level = None  # Autocommit mode
    c = conn.cursor()
    
    # Enable WAL mode for better locking
    c.execute("PRAGMA journal_mode=WAL")
    
    # Delete all data
    tables = ['books', 'categories', 'users']
    for table in tables:
        try:
            c.execute(f"DELETE FROM {table}")
            c.execute("COMMIT")
            print(f"✓ Cleared {table}")
        except Exception as e:
            print(f"⚠ Could not clear {table}: {e}")
    
    # Try to reset sequences
    try:
        c.execute("DELETE FROM sqlite_sequence")
        c.execute("COMMIT")
        print(f"✓ Reset auto-increment")
    except:
        pass
    
    conn.close()
    
    print("\n✅ Database cleared successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
