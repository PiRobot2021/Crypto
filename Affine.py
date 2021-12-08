#!/usr/bin/env python3
"""
AFFINE CIPHERS
Class of single-substitution ciphers with key pairs, following the formula.
Common rotation ciphers (e.g. ROT13) fall in this category.

L * a + b (mod N)

L = letter of plaintext
N = lenght of alphabet
a = multiplier key, coprime of modulus
b = adder key

Key space = 182
Key 1 (modulus coprimes) = 7 (for english alphabet)
Key 2 = 26

Usage:
to encrypt a plaintext: -e KEY1 KEY2 plaintext
to decrypt through all possible keys: -d ciphertext
to find coprime key1 values to the modulus: -k
"""

from sys import argv
import string
from primePy import primes
from sympy import mod_inverse


alphabet= [i for i in string.ascii_lowercase]
ALPHABET= [i for i in string.ascii_uppercase]
mod= len(alphabet)                                                              # Size of modulus


def coprimes():
    p= set(primes.between(1, mod))                                              # List primes until limit mod
    factors_az= {i for i in range(1, mod) if mod % i == 0}                      # List factors of modulus
    return p - factors_az                                                       # Returns coprimes by exclusion set between primes and modulus factors


def encrypt(key1, key2, plaintext):
    cipher= ''
    for l in plaintext:
        if l in alphabet:
            rot= (alphabet.index(l) * key1 + key2) % mod                        # Rotation (L * a + b) (mod 26) for lower case letters
            cipher+= alphabet[rot]
        elif l in ALPHABET:
            rot= (ALPHABET.index(l) * key1 + key2) % mod                        # Rotation (L * a + b) (mod 26) for upper case letters
            cipher+= ALPHABET[rot]
        else:
            cipher+= l
    print(cipher.replace(' ', ''))


def decrypt(cipher):
    for key1 in coprimes(mod):
        for key2 in range(mod):
            plaintext= ''
            for l in cipher:
                if l in alphabet:
                    rot= (mod_inverse(key1, mod) * (alphabet.index(l) - key2)) % mod # Rotation (a^-1 * (L - b) (mod 26) for lower case letters
                    plaintext+= alphabet[rot]
                elif l in ALPHABET:
                    rot= (mod_inverse(key1, mod) * (ALPHABET.index(l) - key2)) % mod # Rotation (a^-1 * (L - b) (mod 26) for upper case letters
                    plaintext+= ALPHABET[rot]
                else:
                    plaintext+= l
            print(key1, key2, plaintext)


def main():
    if argv[1] == '-e' and len(argv) > 3:                                       # Encrypting with -e option
        if int(argv[2]) in coprimes(len(string.ascii_lowercase)):               # Cheking if the multiplier key (KEY1) is a coprime of the modulus
            plaintext= ' '.join(argv[i] for i in range(4, len(argv)))           # If multiple words are given, they are merged into a string
            encrypt(int(argv[2]), int(argv[3]), plaintext)                      # Encrypt using the KEY1 (argv[2]) and KEY2 (argv[3]), casted as integers. 
        else:
            print('KEY1 must be coprime of the modulus, check for possible values with -k')
    elif argv[1] == '-d':                                                       # Decrypting with -d option
        cipher= ' '.join(argv[i] for i in range(2, len(argv)))                  # If the ciphertext contains multiple words, they are mergeed into a string
        decrypt(cipher)                                                         
    elif argv[1] == '-k':
        print(coprimes())                                                       # Display possible values of KEY1
    else:
        print('To encrypt a plaintext through two integer keys: Affine.py -e KEY1 KEY2 plaintext')
        print('To decrypt a ciphertext: Affine.py -d ciphertext')


main()
