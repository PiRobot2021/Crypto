#!/usr/bin/env python3
"""
ALTBASH CIPHER
Used by Hebrew scribes to encrypt the biblical book of Jeremiah.
It reverses the order of the letters in the alphabet (single substitution).

Key space: 26

Usage:
to encrypt a plaintext: -e plaintext
to decrypt through all possible letter rotations: -d ciphertext
"""

from sys import argv
import string
from collections import deque


def encrypt(plaintext):
    shift= deque([l for l in string.ascii_lowercase])
    shift.reverse()
    rotation_tab= plaintext.maketrans(string.ascii_lowercase, ''.join(shift))
    cipher= plaintext.translate(rotation_tab)
    
    SHIFT= deque([L for L in string.ascii_uppercase])
    SHIFT.reverse()
    rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
    print(cipher.translate(rotation_tab))


def decrypt(cipher):
    shift= deque([l for l in string.ascii_lowercase])
    shift.reverse()
    rotation_tab= cipher.maketrans(string.ascii_lowercase, ''.join(shift))
    cipher= cipher.translate(rotation_tab)
    
    SHIFT= deque([L for L in string.ascii_uppercase])
    SHIFT.reverse()
    rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
    print(cipher.translate(rotation_tab))


def main():
    if argv[1] == '-e':
        encrypt(' '.join(argv[i] for i in range(2, len(argv))))
    elif argv[1] == '-d':
        decrypt(' '.join(argv[i] for i in range(2, len(argv))))
    else:
        print('To encrypt a plaintext : Altbash.py -e plaintext')
        print('To decrypt a cipher: Altbash.py -d ciphertext')

main()
