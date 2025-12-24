import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'app.db')

try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Delete all data from tables
    c.execute("DELETE FROM books")
    c.execute("DELETE FROM categories")
    c.execute("DELETE FROM users")
    
    # Reset auto-increment counter
    c.execute("DELETE FROM sqlite_sequence WHERE name='books'")
    c.execute("DELETE FROM sqlite_sequence WHERE name='categories'")
    c.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    
    conn.commit()
    conn.close()
    
    print("✓ Semua data dihapus")
    print("✓ Database berhasil di-reset (kosong)")
    
except sqlite3.Error as e:
    print(f"✗ Error: {e}")
