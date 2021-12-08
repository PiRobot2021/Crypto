#!/usr/bin/env python3
"""
ALTBASH CIPHER
Used by Hebrew scribes to encrypt the biblical book of Jeremiah.
It simply reverses the order of the letters in the alphabet (single substitution).

Key space: 26

Usage:
to encrypt a plaintext: -e plaintext
to decrypt through all possible letter rotations: -d ciphertext
"""

from sys import argv
import string


def encrypt_decrypt(text):
    az= [l for l in string.ascii_lowercase]
    az.reverse()
    za= ''.join(az)

    AZ= [l for l in string.ascii_uppercase]
    AZ.reverse()
    ZA= ''.join(AZ)

    rotation_tab= text.maketrans(string.ascii_lowercase, za)
    reverse= ext.translate(rotation_tab)
    rotation_tab= text.maketrans(string.ascii_uppercase, ZA)
    print(reverse.translate(rotation_tab))


def main():
    if argv[1] == '-e':
        text= ' '.join(argv[i] for i in range(2, len(argv)))                
        encrypt_decrypt(text)
    elif argv[1] == '-d':
        cipher= ' '.join(argv[i] for i in range(2, len(argv)))
        decrypt_decrypt(cipher)
    else:
        print('To encrypt a plaintext : Altbash.py -e plaintext')
        print('To decrypt a cipher: Altbash.py -d ciphertext')

main()
