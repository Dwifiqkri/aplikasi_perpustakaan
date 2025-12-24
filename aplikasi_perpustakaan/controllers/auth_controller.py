# controllers/auth_controller.py
from models.user_model import get_user

def login_user(username, password):
    return get_user(username, password)
