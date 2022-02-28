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
    cipher = text.translate(rot_tab)                                                 # Apply the alphabet translation
    
    AZ_deque = deque([L for L in string.ascii_uppercase])                            # Rotate separately the upper case ascii alphabet
    AZ_deque.rotate(rot)
    new_alphabet = ''.join(AZ_deque)
    
    rot_tab = cipher.maketrans(string.ascii_uppercase, new_alphabet)
    return cipher.translate(rot_tab)


    
def decrypt(cipher, solution):
    for rot in range(26):
        text = encrypt(rot, cipher)
        if text == solution:                                                         # Easier to visualize, just for the learning
            print(rot, '\t', text, '<-')
        else:
            print(rot, '\t', text)
            
            
def main():
    # Encryption
    text = input('Type your text: ')
    text = text.replace(' ', '')
    
    key = input('Enter a numeric key: ')
    assert(int(key).isdigit())
    
    cipher = encrypt(int(key), text)
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i = input('Do you want to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher, text)

if __name__ == '__main__':
    main()
