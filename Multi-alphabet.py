#!/usr/bin/env python3
"""
MULTI-ALPHABET SUBSTITUTION CIPHER
Like a Cesar cipher, with an additional arbitrary shift of letters to obfuscate frequency analysis.
A secret key is provided together with the plaintext and the two are overlapped.
Each letter of the plaintext rotates by the corresponding digit in the key. 
When the key reaches the end, it starts again from the first digit, until all the plaintext is encrypted.
This way wach letter rotates independently from the others, preventing frequency analysis.

key space = 26 * length text

Usage:
to encrypt a plaintext: -e plaintext
to decrypt a ciphertext: -d ciphertext (W.I.P.)
"""


from sys import argv
import string

az= [i for i in string.ascii_lowercase]                             # Create a list of letters in lower ascii 
AZ= [i for i in string.ascii_uppercase]                             # Create a list of letters in upper ascii


def encrypt(key, plaintext):
    key= [int(i) for i in key]                                      # Split the input key into a list of digits
    cipher= ''
    for i, l in enumerate(plaintext):
        key_rot= key[i % len(key)]                                  # Apply key rotation syncronized with the index "i" of the letter in the plaintext
        if l in az:
            cipher+= az[(i + key_rot) % len(az)]                    # Apply the key rotation to the letter in the alphabet (lower ascii)
        elif l in AZ:
            cipher+= AZ[(i + key_rot) % len(AZ))]                   # Apply the key rotation to the letter in the alphabet (upper ascii)
        else:
            cipher+= l                                              # Leave all the other characters (digits, punctuations, etc.) untouched
    print(cipher)
    
    
def decrypt(cipher):
    print('Work in progress')


def main():
    if argv[1] == '-e' and len(argv) > 2:
        encrypt(argv[2], ' '.join(argv[i] for i in range(3, len(argv))))
    elif argv[1] == '-d':
        decrypt(' '.join(argv[i] for i in range(2, len(argv))))
    else:
        print('To encrypt a plaintext using a numeric key: Multi_alphabet.py -e KEY "plaintext and more plaintext"')
        print('To decrypt a ciphertext: Multi_alphabet.py -d ciphertext')

main()
