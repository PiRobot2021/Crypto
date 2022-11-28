#/usr/bin/env python3
"""
GRONSFELD CIPHER
It's a variation of Vigenere cipher, where the table consists only of 10 row (using integer indexes from 0 to 9).
At each row the alphabet rotates left by one position, then the rows are shuffled.

The encryption proceeds by finding each letter of plaintext in the Gronsfeld rows, in ascending order (from 0 to 9),
and add to the cipher the corresponding letter in the column name. Once the rows reach the end, restart from row 0.
"""

import pandas as pd
import string
from collections import deque

TEXT = 'Type your text here...'
SHUFFLED = True

def create_Gronsfeld():                                                                                 # Function to create a Gronsfeld table
    alphabet = deque(string.ascii_lowercase)                                                            # I use a deque to rotate the alphabet
    table = pd.DataFrame(index=range(10), columns=list(string.ascii_uppercase))                         # Create an empty DataFrame in pandas
    for i in range(10):
        table.loc[i] = alphabet                                                                         # Load the alphabet row by row, rotating it left at each step of the loop
        alphabet.rotate(-1)
    if SHUFFLED:
        table = table.sample(frac=1)                                                                    # Shuffle the rows
        table = table.reset_index(drop=True)                                                            # Reset the index and drop the old one, change to drop= False to track the original index
    return table


def get_column(table, letter, row):
    return table.loc[row].where(table.loc[row] == letter).dropna().index[0]                             # Find the column by truth table of letter present in row


def encrypt(text):
    Gronsfeld = create_Gronsfeld()
    print(f'Gronsfeld table:\n{Gronsfeld}')
    enc_text = ''
    j = 0
    for i in text:
        enc_text += get_column(Gronsfeld, i, j % 10)                                                    # Obtain column index from Gronsfeld table, rotating through the columns
        j += 1
    return enc_text


if __name__ == '__main__':
    for i in ''.join([string.punctuation, ' ']):
        TEXT = TEXT.replace(i, '')
    assert(TEXT.isalpha())

    enc_text = encrypt(TEXT)
    print(f'\nCiphertext: {enc_text}')
