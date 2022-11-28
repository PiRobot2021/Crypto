#/usr/bin/env python3
"""
VERNAM CIPHER
It's a historical one-time pad cipher obtained by logical XOR between plaintext and a key with the same length.
"""

import string
import secrets
#from operator import xor

TEXT = 'Type your text here...'


def generate_key(length):
    return ''.join([secrets.choice(string.ascii_letters + string.digits) for i in range(length)])      # Generate a random string (letters and digits) of the length of the plaintext


def encrypt(text, key):
    return ''.join([chr(text[i] ^ key[i]) for i in range(len(key))]).encode()                          # Merge the XOR values into an encoded string 
        

if __name__ == '__main__':
    text = TEXT.replace(' ', '').lower()
    key = generate_key(len(text))
    print(f'Random key: {key}')    
    enc_text = encrypt(text.encode(), key.encode())
    print(f'\nCiphertext: {enc_text}')
