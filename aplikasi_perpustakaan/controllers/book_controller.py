from models.book_model import (
    create_table,
    add_book,
    get_all_books,
    update_book,
    delete_book
)

create_table()

def create_book(title, author, stock, image_path, category_id=None, publisher=None, year=None):
    add_book(title, author, stock, image_path, category_id, publisher, year)

def fetch_books():
    return get_all_books()

def edit_book(book_id, title, author, stock, category_id=None, publisher=None, year=None):
    # Map parameters to model.update_book signature: (book_id, title, author, stock, publisher, year, category_id)
    update_book(book_id, title, author, stock, publisher, year, category_id)

def remove_book(book_id):
    delete_book(book_id)
