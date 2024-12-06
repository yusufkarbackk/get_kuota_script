from cryptography.fernet import Fernet
import json
import os
import sys

password = sys.argv[1]
trimedPassword = password.replace(" ", "")

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt(password):
  
    originalString = password

    encrypted_String = cipher.encrypt(originalString.encode())

    print(f"encrypted: {encrypted_String}")
    #return encrypted_String
    
    
def decrypt(encrypted_string):
    decrypted_string = cipher.decrypt(encrypted_string).decode()
    print(f"decrypted: {decrypted_string}")
    #return decrypted_string

encrypted = encrypt(trimedPassword)
decrypt(encrypted)