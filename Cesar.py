#!/usr/bin/env python3
"""
CESAR CIPHER
First historical cipher (substitution cipher) used by Julius Cesar.
Obtained by shifting all letters of plaintext by 3 positions on the right.
This algorithm let define the amplitude of the rotation.
"""


import string
from collections import deque

az= [l for l in string.ascii_lowercase]
AZ= [L for L in string.ascii_uppercase]


def encrypt(rot, plaintext):
    shift= deque(az)                                                                    # Create a deque of the alphabet
    shift.rotate(rot)                                                                   # Shift the deque
    rotation_tab= plaintext.maketrans(string.ascii_lowercase, ''.join(shift))           # Bulid a translation table
    cipher= plaintext.translate(rotation_tab)                                           # Apply the alphabet shift
    SHIFT= deque(AZ)
    SHIFT.rotate(rot)
    rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
    return cipher.translate(rotation_tab).replace(' ', '')

    
def decrypt(cipher):
    for rot in range(26):
        shift= deque(az)
        shift.rotate(rot)
        rotation_tab= cipher.maketrans(string.ascii_lowercase, ''.join(shift))
        cipher= cipher.translate(rotation_tab)
        
        SHIFT= deque(AZ)
        SHIFT.rotate(rot)
        rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
        print(rot, '\t', cipher.translate(rotation_tab))


def main():
    # Encryption
    text= input('Type your text: ')
    key= input('Enter a numeric key: ')
    assert(key.isdigit())
    cipher= encrypt(int(key), text)
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i= input('Do you want to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher)

main()
