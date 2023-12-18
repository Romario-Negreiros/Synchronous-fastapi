from passlib.hash import pbkdf2_sha256 as crypt

def verify_password(password: str, password_hash: str) -> bool:
    return crypt.verify(password, password_hash)

def generate_password_hash(password: str) -> str:
    return crypt.hash(password)
