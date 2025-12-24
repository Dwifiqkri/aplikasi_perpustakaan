import sqlite3
import os

# Use database in temp directory to avoid file locking issues
DB_DIR = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp', 'perpustakaan_app')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'app.db')

def get_connection():
    # Ensure containing directory exists
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            stock INTEGER,
            image_path TEXT,
            category_id INTEGER,
            publisher TEXT,
            year INTEGER
        )
    """)
    conn.commit()

    # Ensure column 'category_id' exists for older DBs
    try:
        c.execute("PRAGMA table_info(books)")
        cols = [r[1] for r in c.fetchall()]
        # Add any missing columns for backward compatibility
        if 'category_id' not in cols:
            c.execute("ALTER TABLE books ADD COLUMN category_id INTEGER")
            conn.commit()
            cols.append('category_id')
        if 'publisher' not in cols:
            c.execute("ALTER TABLE books ADD COLUMN publisher TEXT")
            conn.commit()
            cols.append('publisher')
        if 'year' not in cols:
            c.execute("ALTER TABLE books ADD COLUMN year INTEGER")
            conn.commit()
            cols.append('year')
    except Exception:
        pass
    conn.close()

def add_book(title, author, stock, image_path, category_id=None, publisher=None, year=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO books (title, author, stock, image_path, category_id, publisher, year) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, author, stock, image_path, category_id, publisher, year)
    )
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, author, stock, image_path, category_id, publisher, year FROM books")
    rows = c.fetchall()
    conn.close()
    return rows

def update_book(book_id, title, author, stock, publisher=None, year=None, category_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE books SET title=?, author=?, stock=?, publisher=?, year=?, category_id=? WHERE id=?",
        (title, author, stock, publisher, year, category_id, book_id)
    )
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

# Alias untuk kompatibilitas file lama
def create_book_table():
    create_table()
