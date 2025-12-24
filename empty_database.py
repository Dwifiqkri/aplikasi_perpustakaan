import sqlite3
from models.book_model import DB_PATH

print(f'Database path: {DB_PATH}')

try:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    
    # Delete all data
    c.execute("DELETE FROM books")
    c.execute("DELETE FROM categories")
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM sqlite_sequence")
    
    conn.commit()
    conn.close()
    
    print("✓ All data cleared")
    print("✓ Auto-increment counters reset")
    
    # Verify
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM books")
    books = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM categories")
    cats = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]
    conn.close()
    
    print(f"\nDatabase status:")
    print(f"  Books: {books} records")
    print(f"  Categories: {cats} records")
    print(f"  Users: {users} records")
    print(f"\n✅ Database is FRESH and EMPTY!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
