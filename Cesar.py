#!/usr/bin/env python3
"""
CESAR CIPHER
First historical cipher (substitution cipher).
Obtained by shifting all letters of plaintext by 3 positions on the right.
This algorithm let define the amplitude of the rotation.

Key space = 26

Usage:
to encrypt a plaintext: -e ROT plaintext
to decrypt through all possible letter rotations: -d ciphertext
"""

from sys import argv
import string
from collections import deque




def encrypt(rot, plaintext):
    shift= deque([l for l in string.ascii_lowercase])
    shift.rotate(rot)
    rotation_tab= plaintext.maketrans(string.ascii_lowercase, ''.join(shift))
    cipher= plaintext.translate(rotation_tab)
    
    SHIFT= deque([L for L in string.ascii_uppercase])
    SHIFT.rotate(rot)
    rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
    print(cipher.translate(rotation_tab))

def decrypt(cipher):
    for rot in range(26):
        shift= deque([l for l in string.ascii_lowercase])
        shift.rotate(rot)
        rotation_tab= cipher.maketrans(string.ascii_lowercase, ''.join(shift))
        cipher= cipher.translate(rotation_tab)
        
        SHIFT= deque([L for L in string.ascii_uppercase])
        SHIFT.rotate(rot)
        rotation_tab= cipher.maketrans(string.ascii_uppercase, ''.join(SHIFT))
        print(rot, '\t', cipher.translate(rotation_tab))



def main():
    if argv[1] == '-e' and len(argv) == 4:
        encrypt(int(argv[2]), argv[3])
    elif argv[1] == '-d' and len(argv) == 3:
        decrypt(argv[2])
    else:
        print('To encrypt a plaintext with rotation (example 13): Cesar.py -e 13 plaintext')
        print('To decrypt through all possible 26 rotations: Cesar.py -d ciphertext')

main()
