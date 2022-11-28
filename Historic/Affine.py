#!/usr/bin/env python3

"""
AFFINE CIPHER
Class of single-substitution ciphers with key pairs, following the formula: L * a + b (mod N)

L = letter of plaintext
N = length of alphabet
a = numeric key (it must be coprime of N, usually a number lower than N)
b = numeric key (usually between 1 and N, higher values will be reduced anyway to this range (thourgh mod N))

"""

import string
from primePy import primes
from sympy import mod_inverse
import secrets


TEXT = 'Type your text here...'

alphabet = list(string.ascii_lowercase)                                                 # I decided to process lower case and upper case letters independently
ALPHABET = list(string.ascii_uppercase)
MOD = len(alphabet)                                                                     # The modulus is the length of the alphabet (26 for English)


def coprimes():
    p = set(primes.between(1, MOD))                                                     # List all the primes lower than the modulus
    divide_az = {i for i in range(1, MOD) if (MOD % i) == 0}                            # List all the dividends of the modulus
    return list(p - divide_az)                                                          # Returns coprimes by logic exclusion between primes lower than modulus and modulus dividends


def encrypt(key1, key2, text):
    enc_text = ''
    for l in text:
        if l in alphabet:
            rot = (alphabet.index(l)*key1 + key2) % MOD                                 # Rotation (L*a + b) (mod N) for lower case letters
            enc_text += alphabet[rot]
        elif l in ALPHABET:
            rot = (ALPHABET.index(l)*key1 + key2) % MOD                                 # Rotation (L*a + b) (mod N) for upper case letters
            enc_text += ALPHABET[rot]
        else:
            enc_text += l
    return enc_text


def decrypt_bruteforce(enc_text):
    for key1 in coprimes():
        for key2 in range(MOD):
            text = ''
            for l in enc_text:
                if l in alphabet:
                    rot = (mod_inverse(key1, MOD) * (alphabet.index(l)-key2)) % MOD   # Rotation (a^-1 * (L-b) (mod 26) for lower case letters
                    text += alphabet[rot]
                elif l in ALPHABET:
                    rot = (mod_inverse(key1, MOD) * (ALPHABET.index(l)-key2)) % MOD   # Rotation (a^-1 * (L-b) (mod 26) for upper case letters
                    text += ALPHABET[rot]
                else:
                    text += l
                print(f'{key1}\t{key2}\t{text}')


if __name__ == '__main__':
    # Encryption

    text = TEXT.replace(' ', '')
    key1 = secrets.choice(coprimes())                                                  # Generate a random key, chosen among coprimes of N
    print(f'First random key, coprime of {MOD}: {key1}')
    
    key2 = secrets.choice(range(1, 26))                                                # Generate a random key between 1 and N
    print(f'Second random key from 1 to {MOD}: {key2}') 
    enc_text = encrypt(key1, key2, text)                                               # Encrypt using the keys casted as integers 
    print(f'\nCiphertext: {enc_text}\n')
    
    # Decryption
    decrypt_bruteforce(enc_text)                                                        # It's a basic bruteforce
