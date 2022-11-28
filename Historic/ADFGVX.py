
#!/usr/bin/env python3
"""
ADFGX and ADFGVX CIPHERS

They are basically variations of the Polybius square, combined with a columnar trnasposition.

In the ADFGX variation, first a Polybius square is built with a shuffled alphabet, replacing the coordinates with the letters ADFGX.
The encryption proceeds as in the classic Polybius square, generating a sequence of letters A, D, F, G and X instead of digits.

This text then place row by row in a square matrix according to a key length.
The encyrption continues as in the columnar cipher.

The ADFGVX variation proceeds in the same order, the only difference is that the Polybius square is 6x6 in this case, 
allowing for the whole alphabet and digits to be used.

Here below I code the ADFGVX variation.

"""

import string
import secrets
import numpy as np
import pandas as pd


TEXT = 'Type your text here...'
LEN_KEY = 5                                                                         # Key length used in the random generator for the columnar encryption
PADDING_CHAR = '_'                                                                  # Used in the columnar encryption to fit the text in a matrix


def create_square():                                                                # Creates a 6x6 Polybius square containing shuffled lower ascii letters and digits
    linear_values = list(string.digits + string.ascii_lowercase)
    shuffled_values = []
    while len(linear_values) > 0:
        i = secrets.choice(linear_values)
        shuffled_values.append(i)
        linear_values.pop(linear_values.index(i))    
    return np.char.asarray(shuffled_values).reshape(6, 6)


def find_coords(square, letter):                                                    # Find the coordinates of a plaintext char in the 6x6 Polybius square and convert them
    ADFGVX = dict(zip(range(6), list('ADFGVX')))                                    # Dictionary used for conversion of integers to letters ADFGVX
    coords = np.where(square == letter)
    return ADFGVX[coords[0][0]] + ADFGVX[coords[1][0]]


def ADFGVX_encrypt(text):                                               
    square = create_square()
    print(f'\nADFGVX random square:\n{square}')
    return ''.join([find_coords(square, i) for i in text])
                                                                                                

def to_table(text, key):                                                            # Tables the plaintext before the columnar encryption
    table = pd.DataFrame(columns= range(len(key)))                                  # Create empty table, with columns from "0" to the length of the key
    while len(text) % len(key) != 0:                                                # Pad the text and the tail, to fit into the table
        text += PADDING_CHAR
    j = 0
    for i in range(0, len(text), len(key)):                                         # Split the text in chunks as long as the key length, and load them into the rows of the table
        chunk = list(text[i:i + len(key)])
        table.loc[j] = chunk
        j += 1
    return table


def to_index(key):                                                                  # Sorts and indexes the key for the columnar encryption
    sorted_key_chars = sorted(key)
    ascending_int = list(range(len(key)))
    ordered_key = list(zip(sorted_key_chars, ascending_int))                        # list of tuples containing sorted key chars and growing int values by steps of 1
    result = []
    for x in key:
        for y in ordered_key:
            if y[0] == x:
                result.append(y)
                ordered_key.remove(y)                                               # Removing the tuple from the ordered_key to avoid duplications in the next key values
                break                                                               # Once value is found, stop rotating through the ordered_keys
    return result


def columnar_encrypt(text, key):
    print(f'\nIntermediate cipher: {text}')
    table = to_table(text, key)                                                     # Table the text
    print(f'\nSquared intermediate cipher:\n{table}')
    print(f'\nRandom key: {key}')
    key = to_index(key)                                                             # Convert the key from string into sorted tuples containing the ordered values of the key chars
    print(f'Sorted key: {key}')  
    enc_text = ''
    for column in key:
        enc_text += ''.join(table[column[1]])                                       # Encrypt by proceeding through each column, in the order given by the ranked key chars
    return enc_text.replace(PADDING_CHAR, '')                                       # Remove the padding chars
    
    
def encrypt(text, key):
    intermediate_cipher = ADFGVX_encrypt(text)
    return columnar_encrypt(intermediate_cipher, key)


if __name__ == '__main__':
    for i in ''.join([string.punctuation, ' ']):
        TEXT = TEXT.replace(i, '')
    key = ''.join([secrets.choice(string.ascii_lowercase) for i in range(LEN_KEY)])
    enc_text = encrypt(TEXT.lower(), key)
    print(f'\nCiphertext: {enc_text}')
