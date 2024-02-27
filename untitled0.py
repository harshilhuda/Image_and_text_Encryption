# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:08:09 2023

@author: pravin
"""

from cryptography.fernet import Fernet
key = Fernet.generate_key()
print("Key : ", key.decode())
f = Fernet(key)
encrypted_data = f.encrypt(b"Hi My name is mrunal")
print("After encryption : ", encrypted_data)
decrypted_data = f.decrypt(encrypted_data)
print(decrypted_data)
print("After decryption : ", decrypted_data.decode())