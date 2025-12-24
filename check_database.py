import sqlite3
from models.book_model import DB_PATH
import os

print(f'Database path: {DB_PATH}')
print(f'File exists: {os.path.exists(DB_PATH)}')
print(f'File size: {os.path.getsize(DB_PATH)} bytes')

try:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    
    # Check tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    table_names = [t[0] for t in tables]
    print(f'\nTables: {table_names}')
    
    # Check data
    for table in ['books', 'categories', 'users']:
        if table in table_names:
            c.execute(f'SELECT COUNT(*) FROM {table}')
            count = c.fetchone()[0]
            print(f'{table.capitalize()}: {count} records')
    
    conn.close()
    print('\n✓ Database is working!')
    
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
