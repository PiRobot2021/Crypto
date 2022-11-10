#/usr/bin/env python3
"""
BIFID CIPHER
It combines a Polybius square substitution with a railfence transposition cipher.
At the end of the encryption, the coordinates are converted back to letter using the same square.
The implementation below uses a 5x5 Polybius square (6x6 could also be implemented) combined with a 2 rails railfence cipher (multiple rails could also be implemented). 
"""

import numpy as np
import random
import string


def create_Polybius():
    az = [i for i in string.ascii_lowercase if i != 'j']                            # "j" is omitted in this case. A variation could be to remove "q" instead.
    random.shuffle(az)                                                              # Randomize the order of the letters
    return np.char.array(az, unicode=True).reshape((5, 5))                          # Creating the Polybius square for letters in lower ascii.


def railfence(square, text):
    x = []
    y = []
    for i in text:
        pair = np.where(square == i)
        x.append(pair[0][0])
        y.append(pair[1][0])
    return x + y


def encrypt(text):
    square = create_Polybius()
    print(f'\nRandom Polybius square:\n{square}')
    coords = railfence(square, text)
    print(f'\nPolybius coordinates transposed through railfence cipher:\n{coords}')
    return ''.join([square[coords[i], coords[i + 1]] for i in range(len(coords) - 1)])


def main():
    text = input('Type your text (letters only): ')
    text = text.replace(' ', '').lower()
    assert(text.isalpha())

    enc_text = encrypt(text)
    print(f'\nCiphertext: {enc_text}')

if __name__ == '__main__':
    main()
