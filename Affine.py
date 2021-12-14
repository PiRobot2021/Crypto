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
"""

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
    return cipher.replace(' ', '')


def decrypt(cipher):
    print('K1\tK2\tTENTATIVE')
    for key1 in coprimes():
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
            print(f'{key1}\t{key2}\t{plaintext}')


def main():
    # Encryption
    text= input('Type your text: ')
    
    key1= input(f'Chose the first numeric key {coprimes()}: ') 
    assert(key1 not in coprimes())                                              # Cheking if the multiplier key (KEY1) is a coprime of the modulus

    key2= input('Type the second numeric key: ')
    cipher= encrypt(int(key1), int(key2), text)                                 # Encrypt using the keys casted as integers 
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i= input('Want to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher)                                                         

main()
