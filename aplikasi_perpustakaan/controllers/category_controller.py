from models.category_model import (
    create_table,
    add_category,
    get_all_categories,
    update_category,
    delete_category
)

# pastikan tabel dibuat
create_table()

def create_category(name):
    add_category(name)

def fetch_categories():
    return get_all_categories()

def edit_category(category_id, name):
    update_category(category_id, name)

def remove_category(category_id):
    delete_category(category_id)
