from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Key for AES encryption
KEY = b'Sixteen byte key'

# Encrypt string


def encrypt_string(plain_text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct  # Combine IV and ciphertext

# Decrypt string


def decrypt_string(encrypted_text: str) -> str:
    iv = base64.b64decode(encrypted_text[:24])  # Decode IV
    ct = base64.b64decode(encrypted_text[24:])  # Decode ciphertext
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted_data.decode('utf-8')
