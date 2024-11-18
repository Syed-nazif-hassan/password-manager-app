from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from dotenv import dotenv_values

# Reload the .env file
env_values = dotenv_values('.env')

# Access the encryption key from the reloaded .env file
encoded_key = env_values.get('ENCRYPTION_KEY')

# Decode the encryption key to binary format
KEY = base64.b64decode(encoded_key)

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
