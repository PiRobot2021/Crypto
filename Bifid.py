#/usr/bin/env python3
"""
BIFID CIPHER
It combines a Polybius square substitution with a railfence transposition cipher.
At the end of the encryption, the coordinates are converted back to letter using the same square.
"""

import numpy as np
import random
import string


def create_Polybius():
    az = [i for i in string.ascii_lowercase if i != 'j']                            # "j" is omitted in this case. A variation could be to remove "q" instead.
    random.shuffle(az)                                                              # Randomize the order of the letters
    return np.char.array(az, unicode = True).reshape((5, 5))                        # Creating the Polybius square for letters in lower ascii.


def railfence(square, text):
    x = []
    y = []
    for i in text:
        pair = np.where(square == i)
        x.append(pair[0][0])
        y.append(pair[1][0])
    return x + y


def encrypt(text):
    square= create_Polybius()
    print(f'\nRandom Polybius square:\n{square}')
    coords = railfence(square, text)
    print(f'\nPolybius coordinates transposed through Railfence:\n{coords}')
    return ''.join([square[coords[i], coords[i + 1]] for i in range(len(coords) - 1)])


def main():
    text = input('Type your text (letters only): ')
    text = text.replace(' ', '').lower()
    assert(text.isalpha())

    cipher = encrypt(text)
    print(f'\nCipher: {cipher}')

if __name__ == '__main__':
    main()
