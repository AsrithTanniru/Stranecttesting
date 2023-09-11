from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# def decrypt(l):
#     # Convert the hex-encoded cipher text back to bytes
#     cipher_text = bytes.fromhex(l)
#     # cipher_text = d


#     # The same encryption key and IV used for encryption
#     encryption_key = bytes.fromhex("26a3450f19e7a4dbf0fdfe32418e4b675dd039d6280dd60a8c0abb5509c5e59a")
#     iv = bytes.fromhex("523d931c832f6ac594bd2af8964a1078")

#     # Create a cipher object using AES in CBC mode with the specified encryption key and IV
#     cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())

#     # Decrypt the data
#     decryptor = cipher.decryptor()
#     decrypted_padded_data = decryptor.update(cipher_text) + decryptor.finalize()

#     # Unpad the decrypted data
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

#     # Return the decrypted data as a string
#     return decrypted_data.decode('utf-8')

# # Example usage
# # encrypted_text = "9f6aff392c2cffe4304a2f468916752ecf900927fdc12ec8b2bcbcd71568a0c505e9971dd31d1e562ae192ead081426abce9772a7a1f1f99f235c0db32148ce7"  # Replace with the actual hex-encoded encrypted text
# # decrypted_text = decrypt(encrypted_text)
# # print("Decrypted text:", decrypted_text)


def decrypt(l):
    try:
        # Print the input string to see its contents
        print("Input String:", l)
        
        # Convert the hex-encoded cipher text back to bytes
        cipher_text = bytes.fromhex(l)
        
        # The same encryption key and IV used for encryption
        encryption_key = bytes.fromhex("26a3450f19e7a4dbf0fdfe32418e4b675dd039d6280dd60a8c0abb5509c5e59a")
        iv = bytes.fromhex("523d931c832f6ac594bd2af8964a1078")

        # Create a cipher object using AES in CBC mode with the specified encryption key and IV
        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())

        # Decrypt the data
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(cipher_text) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        
        # Return the decrypted data as a string
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print("Decryption Error:", e)
        return None
