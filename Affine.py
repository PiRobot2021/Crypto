#!/usr/bin/env python3

"""
AFFINE CIPHER
Class of single-substitution ciphers with key pairs, following the formula: L * a + b (mod N)

L = letter of plaintext
N = lenght of alphabet
a = numeric key (it must be coprime of N, usually a number lower than N)
b = numeric key

"""

import string
from primePy import primes
from sympy import mod_inverse


alphabet= [i for i in string.ascii_lowercase]                                           # I decided to process lower case and upper case letters independently
ALPHABET= [i for i in string.ascii_uppercase]
MOD= len(alphabet)                                                                      # The modulus is the length of the alphabet (26 for English)


def coprimes():
    p= set(primes.between(1, MOD))                                                      # List all the primes lower than the modulus
    divide_az= {i for i in range(1, MOD) if MOD % i == 0}                               # List all the dividends of the modulus
    return p - divide_az                                                                # Returns coprimes by logic exclusion between primes lower than modulus and modulus dividends


def encrypt(key1, key2, plaintext):
    cipher= ''
    for l in plaintext:
        if l in alphabet:
            rot= (alphabet.index(l) * key1 + key2) % MOD                                # Rotation (L * a + b) (mod N) for lower case letters
            cipher+= alphabet[rot]
        elif l in ALPHABET:
            rot= (ALPHABET.index(l) * key1 + key2) % MOD                                # Rotation (L * a + b) (mod N) for upper case letters
            cipher+= ALPHABET[rot]
        else:
            cipher+= l
    return cipher.replace(' ', '')


def decrypt(cipher):
    print('K1\tK2\tTENTATIVE')
    for key1 in coprimes():
        for key2 in range(MOD):
            plaintext= ''
            for l in cipher:
                if l in alphabet:
                    rot= (mod_inverse(key1, MOD) * (alphabet.index(l) - key2)) % MOD    # Rotation (a^-1 * (L - b) (mod 26) for lower case letters
                    plaintext+= alphabet[rot]
                elif l in ALPHABET:
                    rot= (mod_inverse(key1, MOD) * (ALPHABET.index(l) - key2)) % MOD    # Rotation (a^-1 * (L - b) (mod 26) for upper case letters
                    plaintext+= ALPHABET[rot]
                else:
                    plaintext+= l
            print(f'{key1}\t{key2}\t{plaintext}')


def main():
    # Encryption
    text= input('Type your text: ')
    
    key1= input(f'Chose the first numeric key {coprimes()}: ') 
    assert(key1 not in coprimes())                                                      # Cheking if the multiplier key (KEY1) is a coprime of the modulus

    key2= input('Type the second numeric key: ')
    assert(key2.isdigit())
    
    cipher= encrypt(int(key1), int(key2), text)                                         # Encrypt using the keys casted as integers 
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i= input('Want to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher)                                                         

main()
