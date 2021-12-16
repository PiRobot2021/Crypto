#/usr/bin/env python3
"""
HILL CIPHER

Substituion cipher that relies on matrix multiplication.
The plaintext is first converted into integers, with moduls equal to the length of the alphabet used.
The key is a square matrix of the side length equal to the text length, containing random integers using the same modulus.
The cipher is obtained by multiplying the vectorized text and the matrix, always within the same modulus.
The resulting numbers are then converted back to letters.

"""

import string
import numpy as np
import re

# It can be modified to encrypt more ascii characters
MOD= len(string.ascii_lowercase)                                                                        # I extracted the modulus value from the code and linked to the alphabet I use


def create_random(n):
    values= np.random.randint(low= 0, high= MOD, size= n * n)                                           # Create a matrix contaning random integers modulus MOD
    return np.array(values).reshape(n, n)                                                               # Reshape the array in a square with side as long as the text


def custom_print(matrix, vector, cipher):
    print(f'\nMultiply a random square matrix by vectorized text (mod {MOD}):\n')
    for i in range(len(vector)):
        print(f'{matrix[i]}  {vector[i]} \t{cipher[i]}')


def encrypt(text):
    vector= np.array([ord(i) - ord(string.ascii_lowercase[0]) for i in text]).reshape(len(text), 1)     # Convert the plaintext to integers modulus MOD and vectorize it
    matrix= create_random(len(text))                                                                    # Create a matrix with side of the length of text, containing random integers modulus MOD
    cipher= np.mod(np.matmul(matrix, vector), MOD)                                                      # Matrix multiplication, the resulting values are also modulus MOD
    custom_print(matrix, vector, cipher)
    return ''.join(chr(i + ord(string.ascii_lowercase[0])) for i in cipher)


def main():
    text= input('Type your text: ')
    text= re.sub('[\t\s]', '', text.lower())
    assert(text.isalpha())                                                                              # The original cipher allows only letters, but it can be easily customized to encrypt all ascii (mod 127)
    cipher= encrypt(text)
    print(f'\nCipher: {cipher}')

main()
