#!/usr/bin/env python3

"""
AFFINE CIPHER
Class of single-substitution ciphers with key pairs, following the formula: L * a + b (mod N)

L = letter of plaintext
N = lenght of alphabet
a = numeric key (it must be coprime of N, usually a number lower than N)
b = numeric key (usually between 1 and N, higher values will be reduced anyway to this range (thourgh mod N))

"""

import string
from primePy import primes
from sympy import mod_inverse
import random

alphabet= [i for i in string.ascii_lowercase]                                           # I decided to process lower case and upper case letters independently
ALPHABET= [i for i in string.ascii_uppercase]
MOD= len(alphabet)                                                                      # The modulus is the length of the alphabet (26 for English)


def coprimes():
    p= set(primes.between(1, MOD))                                                      # List all the primes lower than the modulus
    divide_az= {i for i in range(1, MOD) if MOD % i == 0}                               # List all the dividends of the modulus
    return list(p - divide_az)                                                                # Returns coprimes by logic exclusion between primes lower than modulus and modulus dividends


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
    return cipher


def decrypt(cipher, solution):
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
            if plaintext == solution:                                                   # This helps visualize the output, just for learning
                print(f'{key1}\t{key2}\t{plaintext} <-')
            else:
                print(f'{key1}\t{key2}\t{plaintext}')

def main():
    # Encryption
    text= input('Type your text: ')
    text= text.replace(' ', '')
    
    key1= random.choices(coprimes(), k= 1)[0]                                           # Generate a random key, chosen among coprimes of N
    print(f'First random key, coprime of {MOD}: {key1}')

    key2= random.randint(1, 26)                                                         # Generate a random key between 1 and N
    print(f'Second random key from 1 to {MOD}: {key2}')
    
    cipher= encrypt(key1, key2, text)                                                   # Encrypt using the keys casted as integers 
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i= input('Want to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher, text)                                                           # It's a basic bruteforce

main()
