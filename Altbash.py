#!/usr/bin/env python3

"""
ALTBASH CIPHER
Used by Hebrew scribes to encrypt the biblical book of Jeremiah.
It simply reverses the order of the letters in the alphabet (single substitution).
"""

import string


def encrypt_decrypt(text):
    az= [l for l in string.ascii_lowercase]
    az.reverse()
    za= ''.join(az)

    AZ= [l for l in string.ascii_uppercase]
    AZ.reverse()
    ZA= ''.join(AZ)

    rotation_tab= text.maketrans(string.ascii_lowercase, za)
    reverse= text.translate(rotation_tab)
    rotation_tab= text.maketrans(string.ascii_uppercase, ZA)
    print(reverse.translate(rotation_tab))


def main():
    text= input('Type your text: ')
    encrypt_decrypt(text)
    
main()
