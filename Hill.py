#/usr/bin/env python3
"""
HILL CIPHER



"""

import string
import numpy as np
import re

MOD= len(string.ascii_lowercase)


def create_random(n):
    values= np.random.randint(low= 0, high= MOD, size= n * n)
    return np.array(values).reshape(n, n)


def custom_print(matrix, vector, cipher):
    print(f'\nMultiply a random square matrix by vectorized text (mod {MOD}):\n')
    for i in range(len(vector)):
        print(f'{matrix[i]}  {vector[i]} \t{cipher[i]}')


def encrypt(text):
    vector= np.array([ord(i) - ord(string.ascii_lowercase[0]) for i in text]).reshape(len(text), 1)
    matrix= create_random(len(text))
    cipher= np.mod(np.matmul(matrix, vector), MOD)
    custom_print(matrix, vector, cipher)
    return ''.join(chr(i + ord(string.ascii_lowercase[0])) for i in cipher)


def main():
    text= input('Type your text: ')
    text= re.sub('[\t\s]', '', text.lower())
    assert(text.isalpha())
    cipher= encrypt(text)
    print(f'\nCipher: {cipher}')

main()
