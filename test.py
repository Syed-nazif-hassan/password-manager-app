import os
import base64

key = os.urandom(16)  # 16 bytes = 128 bits

encoded_key = base64.b64encode(key).decode('utf-8')
print(encoded_key)

KEY = base64.b64decode(encoded_key)  # Decode from base64 to bytes
print(KEY)

