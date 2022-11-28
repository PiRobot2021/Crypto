#!/usr/bin/env python3
"""
POLYBIUS CIPHER
a.k.a. Polybius square, it is a single substitution cipher.
The first step in the classic cipher is to create a 5x5 square matrix containing the alphabet, where "i" and "j" are combined. As a variation, the letter "q" could be removed.
The letters might not be in order, to increase the encryption security.
Each letter is represented by two coordinates in the Polybius square.
It is also possible to use a 6x6 square, with the advantage of hosting the full alphabet and the digits, without loosing information.
"""


import string
import numpy as np
import secrets


TEXT = 'Type your text here...'

polybius_alphabet = [i for i in string.ascii_lowercase if i != 'j']                            # "j" is omitted in this case. A variation could be to remove "q" instead.

az = []
while len(polybius_alphabet) > 0:
    i = secrets.choice(polybius_alphabet)
    az.append(i)
    polybius_alphabet.pop(polybius_alphabet.index(i))

square = np.char.array(az, unicode=True).reshape((5, 5))                        # Creating the Polybius square for letters in lower ascii.


def encrypt(text):
    enc_text = np.empty(0, dtype='int')                                         # Empty array to receive the encrypted letters
    for l in text:
        if l in az:
            xy = np.where(square == l)                                          # Find the coordinates of the letter
            enc_text = np.append(enc_text, xy[0])                               # Append the coordinates to the cipher
            enc_text = np.append(enc_text, xy[1])
    return enc_text


if __name__ == '__main__':
    text = TEXT.replace('j', 'i')                                               
    for i in ''.join([string.punctuation, ' ']):
        text = text.replace(i, '')
    
    # Encryption
    print(f'\nRandom Polybius square:\n{square}')
    enc_text = encrypt(text.lower())                           
    print(f'\nCiphertext: {enc_text}\n')
