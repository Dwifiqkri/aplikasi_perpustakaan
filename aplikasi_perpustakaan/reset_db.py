#!/usr/bin/env python3
"""
Script untuk membuat database baru yang bersih dan proper
dengan WAL mode untuk menghindari lock issues
"""

import os
import sqlite3
import tempfile
import shutil
from pathlib import Path

# Paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(APP_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'app.db')

print("=" * 60)
print("DATABASE RESET UTILITY")
print("=" * 60)

# Step 1: Create database in temp location
print("\n[Step 1] Creating fresh database in temp location...")
temp_db = os.path.join(tempfile.gettempdir(), 'tempdb.db')

# Clean up old temp file if exists
if os.path.exists(temp_db):
    try:
        os.remove(temp_db)
        print(f"  ✓ Cleaned up old temp file")
    except:
        pass

# Create fresh database
conn = sqlite3.connect(temp_db)
conn.execute("PRAGMA journal_mode=WAL")  # Use WAL mode
c = conn.cursor()

# Create tables
c.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        stock INTEGER,
        image_path TEXT
    )
""")

c.execute("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT
    )
""")

conn.commit()
conn.close()
print(f"  ✓ Created fresh database: {temp_db}")

# Step 2: Backup old database
print("\n[Step 2] Backing up old database...")
backup_path = os.path.join(DB_DIR, 'app.db.backup')
if os.path.exists(DB_PATH):
    try:
        if os.path.exists(backup_path):
            os.remove(backup_path)
        shutil.copy2(DB_PATH, backup_path)
        print(f"  ✓ Backed up to: {backup_path}")
    except Exception as e:
        print(f"  ⚠ Warning (non-fatal): {e}")

# Step 3: Replace database
print("\n[Step 3] Installing new database...")
os.makedirs(DB_DIR, exist_ok=True)

# Remove WAL related files if they exist
for ext in ['', '-shm', '-wal']:
    f = DB_PATH + ext
    if os.path.exists(f):
        try:
            os.remove(f)
        except:
            pass

try:
    shutil.move(temp_db, DB_PATH)
    print(f"  ✓ Installed new database: {DB_PATH}")
except Exception as e:
    print(f"  ✗ Move failed: {e}")
    # Try copy as fallback
    try:
        shutil.copy2(temp_db, DB_PATH)
        os.remove(temp_db)
        print(f"  ✓ Installed new database (using copy): {DB_PATH}")
    except Exception as e2:
        print(f"  ✗ Copy failed too: {e2}")
        exit(1)

# Step 4: Verify
print("\n[Step 4] Verifying database...")
try:
    conn = sqlite3.connect(DB_PATH, timeout=5)
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in c.fetchall()]
    
    for table in tables:
        if table != 'sqlite_sequence':
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"  ✓ {table}: {count} records")
    
    conn.close()
except Exception as e:
    print(f"  ✗ Verification failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ DATABASE RESET SUCCESSFUL!")
print("=" * 60)
print(f"Database: {DB_PATH}")
print(f"Status: FRESH & CLEAN (empty tables)")
print("=" * 60)
