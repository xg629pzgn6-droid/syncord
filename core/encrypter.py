from core.setup import get_encryption_key
from cryptography.fernet import Fernet

def encrypted_data(data: bytes) -> bytes:
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    return encrypted

def decrypted_data(data: bytes) -> bytes:
    key = get_encryption_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    return decrypted