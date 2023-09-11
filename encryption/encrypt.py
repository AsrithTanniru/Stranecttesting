from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Your encryption key should be a secure random byte string of appropriate length (e.g., 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
# encryption_key = os.urandom(32)

def encrypt(d):

    # The data you want to encrypt
    data = d

    # Generate a random initialization vector (IV)
    # iv = os.urandom(16)

    encryption_key = bytes.fromhex("26a3450f19e7a4dbf0fdfe32418e4b675dd039d6280dd60a8c0abb5509c5e59a")
    iv = bytes.fromhex("523d931c832f6ac594bd2af8964a1078")

    # Create a cipher object using AES in CBC mode with the specified encryption key and IV
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    # Print the encrypted data and other relevant information
 
    return(cipher_text.hex())


