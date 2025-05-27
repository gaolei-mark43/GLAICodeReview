import os
import hashlib
import base64
from app.config import PASSWORD_HASH_ITERATIONS

def generate_salt(length=16):
    return base64.urlsafe_b64encode(os.urandom(length)).decode()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        PASSWORD_HASH_ITERATIONS
    ).hex() 