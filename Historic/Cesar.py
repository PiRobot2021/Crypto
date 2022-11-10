#!/usr/bin/env python3
"""
CESAR CIPHER
First historical cipher (substitution cipher) used by Julius Cesar.
Obtained by shifting all letters of plaintext by 3 positions on the right.
This algorithm let define the amplitude of the rotation.
"""


import string
from collections import deque


def encrypt(rot, text):
    az_deque = deque([l for l in string.ascii_lowercase])                            # Create a deque of the lower ascii alphabet and rotate it
    az_deque.rotate(rot)
    new_alphabet = ''.join(az_deque)
                                                                  
    rot_tab = text.maketrans(string.ascii_lowercase, new_alphabet)                   # Bulid a translation table
    enc_text = text.translate(rot_tab)                                                 # Apply the alphabet translation
    
    AZ_deque = deque(string.ascii_uppercase)                                         # Rotate separately the upper case ascii alphabet
    AZ_deque.rotate(rot)
    new_alphabet = ''.join(AZ_deque)
    
    rot_tab = enc_text.maketrans(string.ascii_uppercase, new_alphabet)
    return enc_text.translate(rot_tab)


    
def decrypt_bruteforce(enc_text):
    for rot in range(26):
        text = encrypt(rot, enc_text)
        print(rot, '\t', text)
            
            
def main():
    # Encryption
    text = input('Type your text: ')
    text = text.replace(' ', '')
    
    key = input('Enter a numeric key: ')
    assert(int(key).isdigit())
    
    enc_text = encrypt(int(key), text)
    print(f'\nCiphertext: {enc_text}\n')
    
    # Decryption
    decrypt_bruteforce(enc_text)

if __name__ == '__main__':
    main()
