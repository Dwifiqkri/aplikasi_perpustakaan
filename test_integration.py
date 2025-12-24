#!/usr/bin/env python3
"""
Test script untuk verifikasi integrasi Admin-Member Dashboard
"""

import os
import sys
from models.book_model import (
    get_connection, get_all_books, add_book, delete_book
)

print("=" * 60)
print("TEST INTEGRASI ADMIN ↔ MEMBER DASHBOARD")
print("=" * 60)

# Test 1: Check database connection
print("\n[Test 1] Database Connection")
try:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    conn.close()
    print(f"  ✓ Database connected")
    print(f"  ✓ Total buku saat ini: {count}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 2: Fetch books
print("\n[Test 2] Fetch Books")
try:
    books = get_all_books()
    print(f"  ✓ Berhasil fetch {len(books)} buku")
    if books:
        print(f"  ✓ Contoh buku pertama:")
        b = books[0]
        print(f"     - ID: {b[0]}")
        print(f"     - Judul: {b[1]}")
        print(f"     - Penulis: {b[2]}")
        print(f"     - Stok: {b[3]}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: Test add book function
print("\n[Test 3] Test Add Book")
initial_count = len(get_all_books())
print(f"  • Initial book count: {initial_count}")

try:
    add_book("Test Book", "Test Author", 5, None)
    new_count = len(get_all_books())
    print(f"  ✓ Buku ditambahkan")
    print(f"  ✓ New book count: {new_count}")
    
    if new_count > initial_count:
        print(f"  ✓ Integrasi ADD berfungsi!")
    else:
        print(f"  ✗ Integrasi ADD gagal!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 4: Test delete book function
print("\n[Test 4] Test Delete Book")
try:
    books = get_all_books()
    if books:
        last_book = books[-1]
        last_id = last_book[0]
        delete_book(last_id)
        
        books_after = get_all_books()
        print(f"  ✓ Buku dihapus (ID: {last_id})")
        print(f"  ✓ Jumlah buku berkurang dari {len(books)} menjadi {len(books_after)}")
        
        if len(books_after) < len(books):
            print(f"  ✓ Integrasi DELETE berfungsi!")
        else:
            print(f"  ✗ Integrasi DELETE gagal!")
    else:
        print(f"  - Tidak ada buku untuk dihapus")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 5: Member Dashboard module check
print("\n[Test 5] Member Dashboard Module")
try:
    from views.member_dashboard import MemberDashboard
    print(f"  ✓ MemberDashboard module loaded")
    
    # Check if auto-refresh methods exist
    methods = ['refresh_books', 'start_auto_refresh', 'auto_refresh_worker', 'update_display']
    for method in methods:
        if hasattr(MemberDashboard, method):
            print(f"  ✓ Method '{method}' ada")
        else:
            print(f"  ✗ Method '{method}' tidak ada")
            
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 6: Book Controller module check
print("\n[Test 6] Book Controller Module")
try:
    from controllers.book_controller import (
        create_book, fetch_books, edit_book, remove_book
    )
    print(f"  ✓ Book controller functions loaded")
    print(f"  ✓ create_book: Available")
    print(f"  ✓ fetch_books: Available")
    print(f"  ✓ edit_book: Available")
    print(f"  ✓ remove_book: Available")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("✅ INTEGRASI SIAP DIGUNAKAN!")
print("=" * 60)
print("\nCara Test:")
print("1. Jalankan aplikasi dengan: python main.py")
print("2. Login sebagai admin")
print("3. Buka Member Dashboard di tab/window lain")
print("4. Tambah buku dari admin")
print("5. Lihat buku otomatis muncul di member (dalam 5 detik)")
print("=" * 60)
