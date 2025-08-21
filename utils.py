# CyberSecurity involving Password Hashing for the App

import hashlib, secrets, hmac

def generate_salt(hexlen: int = 16) -> str:
    return secrets.token_hex(hexlen)

def hash_password(password: str, salt: str, iterations: int = 100_000) -> str:
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(salt, str):
        salt = salt.encode('utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', password, salt, iterations)
    return dk.hex()

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    computed = hash_password(password, salt)
    return hmac.compare_digest(computed, stored_hash)