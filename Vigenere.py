#!/usr/bin/env python3
"""
VIGENERE CIPHER
It uses the multi-alphabet square of tabula recta combiend with a secret keyword.
The tabula recta is a square table constructed by rotating the alphabet by one left at each row.
It has diagonal simmetry property.

The encryption of each letter is obtained by looking up in the table,
using as coordinates the plaintext letter (x axis) and the corresponding key letter (y axis).

After each letter encryption, the keyword is rotated by one, and when it reaches the end is restarted from the begin, until the all the plaintext is encrypted.
This cipher obfuscates frequency analysis effectively.

Knowing the keyword, the cipher is decrypted by obtaining the row index of the cipher letter in the column indicated by the key character.
The plaintext letter is row index of it.

A variation of this cipher, the "running key cipher" uses a random string of random characters

"""


import string
import random
import pandas as pd
from collections import deque


az= deque([i for i in string.ascii_lowercase])                                  # Creating a deque of the alphabet
tabula= pd.DataFrame(columns= az, index=az)                                     # Building an empty tabula
for i in string.ascii_lowercase:                                                # Filling tabula row by row
    tabula[i]= az
    az.rotate(-1)                                                               # Rotating the deque left by one at each row


def encrypt(key, text):
    cipher= ''
    key= [i for i in key]                                                       # Converint the keyword into a list of characters
    for i, l in enumerate(text):
        k= key[i % len(key)]                                                    # Rotating through the key letters
        if l in az:
            cipher+= tabula.loc[l][k]                                           # Encrypting through the tabula using the plaintext letter "l" and key char "k" as coordinates
        else:
            cipher+= l
    return cipher
    
    
def brute_force(cipher):
    print('Work in progress')


def decrypt(key, cipher):
    text= ''
    key= [i for i in key]
    for i, l in enumerate(cipher):
        k= key[i % len(key)]
        if l in az:
            c= tabula[k].where(tabula[k] == l).dropna()                         # Decrypting by searching at which row index the column of the key "k" has the value of the cipher "l"
            text+= c.index[0]
        else:
            text+= l
    print(text)


def main():
    # Encryption
    text= input('Type your text: ')
    #key= input('Type a secret keyword: ')
    #assert(key.isascii())                                                      # The cipher only works if the keyword contains only ascii characters
    key= ''.join(random.choices(string.ascii_lowercase, k=256))                 # A stronger variation with random key, called "running key cipher"
    cipher= encrypt(key.lower(), text.lower())                                  # The tabula recta is not case sensitive, all letters are turned lower case
    print(f'\nCipher: {cipher}\n')

    # Decryption
    i= input(f'Do you want to decrypt with the key {key}? [y/n]:')
    if i == 'y':
        decrypt(key, cipher)
    #brute_force(cipher)

main()
