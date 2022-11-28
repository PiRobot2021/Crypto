#!/usr/bin/env python3

"""
ALTBASH CIPHER
Classic ancient cipher. It simply reverses the order of the letters in the alphabet (single substitution).
"""

import string


def encrypt_decrypt(text):
    za = string.ascii_lowercase[::-1]
    ZA = string.ascii_uppercase[::-1]

    rotation_tab = text.maketrans(string.ascii_lowercase, za)       # I simply find maketrans cool, it can also be achieved manually
    reverse = text.translate(rotation_tab)
    rotation_tab = text.maketrans(string.ascii_uppercase, ZA)
    print(reverse.translate(rotation_tab).replace(' ', ''))


if __name__ == '__main__':
    text = input('Type your text: ')
    encrypt_decrypt(text)                                           # Being a simple reverse, encryption and decryption proceed with the same function
