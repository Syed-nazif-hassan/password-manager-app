from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Key for AES encryption
KEY = b'Sixteen byte key'

# Encrypt the identifier


def encrypt_identifier(identifier: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(identifier.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct  # Combine IV and ciphertext

# Decrypt the identifier


def decrypt_identifier(encrypted_identifier: str) -> str:
    # First 24 chars are the IV
    iv = base64.b64decode(encrypted_identifier[:24])
    ct = base64.b64decode(encrypted_identifier[24:])  # Rest is the ciphertext
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted_data.decode('utf-8')

# Encrypt the password


def encrypt_password(password: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(password.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct  # Combine IV and ciphertext

# Decrypt the password


def decrypt_password(encrypted_password: str) -> str:
    # First 24 chars are the IV
    iv = base64.b64decode(encrypted_password[:24])
    ct = base64.b64decode(encrypted_password[24:])  # Rest is the ciphertext
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted_data.decode('utf-8')
