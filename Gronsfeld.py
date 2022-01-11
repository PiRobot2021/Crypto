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

SHUFFLED= True

def create_Gronsfeld():                                                                                 # Function to create a Gronsfeld table
    alphabet= deque(list(string.ascii_lowercase))                                                       # I use a deque to rotate the alphabet
    table= pd.DataFrame(index= [i for i in range(10)], columns= [i for i in string.ascii_uppercase])    # Create an empty DataFrame in pandas
    for i in range(10):
        table.loc[i]= alphabet                                                                          # Load the alphabet row by row, rotating it left at each step of the loop
        alphabet.rotate(-1)
    if SHUFFLED:
        table= table.sample(frac= 1)                                                                    # Shuffle the rows
        table= table.reset_index(drop= True)                                                            # Reset the index and drop the old one, change to drop= False to track the original index
    return table


def get_column(table, letter, row):
    return table.loc[row].where(table.loc[row] == letter).dropna().index[0]                             # Find the column by truth table of letter present in row


def encrypt(text):
    Gronsfeld= create_Gronsfeld()
    print(f'Gronsfeld table:\n{Gronsfeld}')
    cipher= ''
    j= 0
    for i in text:
        cipher+= get_column(Gronsfeld, i, j % 10)                                                       # Obtain column index from Gronsfeld table, rotating through the columns
        j+= 1
    return cipher


def main():
    text= input('Type your text (letters only): ')
    text= text.replace(' ', '').lower()
    assert(text.isalpha())

    cipher= encrypt(text)
    print(f'\nCipher: {cipher}')

if __name__ == '__main__':
    main()
