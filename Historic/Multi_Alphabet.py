#!/usr/bin/env python3
"""
MULTI-ALPHABET SUBSTITUTION CIPHER
Similar to Cesar cipher, it adds an arbitrary shift of letters to obfuscate frequency analysis.

A secret key is provided together with the plaintext.
The encryption proceeds by rotating each letter of the plaintext by the corresponding digit in the key. 

When the key reaches the end, it starts again, until all the plaintext is encrypted.
Having each letter rotating by a different value, frequency analysis is obfuscated.
"""


import string
import random

LEN_KEY = 5

az = list(string.ascii_lowercase)                                       # Create a list of letters in lower ascii 
AZ = list(string.ascii_uppercase)                                       # Create a list of letters in upper ascii


def encrypt(key, plaintext):
    enc_text = ''
    for i, j in enumerate(plaintext):
        key_rot = key[i % len(key)]                                       # Apply key rotation syncronized with the index "i" of the letter in the plaintext
        if l in az:
            enc_text += az[(i + key_rot) % len(az)]                       # Apply the key rotation to the letter in the alphabet (lower ascii)
        elif l in AZ:
            enc_text += AZ[(i + key_rot) % len(AZ)]                       # Apply the key rotation to the letter in the alphabet (upper ascii)
        else:
            enc_text += l                                                 # Leave all the other characters (digits, punctuations, etc.) untouched
    return enc_text.replace(' ', '')


if __name__ == '__main__':
    # Encryption
    text = input('Type your text: ')
    key = [random.randint(1, len(az)) for i in range(LEN_KEY)]            # I limited the random key within the modulus, excluding rotation 0
    print(f'Random key: {key}')
    
    enc_text = encrypt(key, text)
    print(f'\nCiphertext: {enc_text}\n')
