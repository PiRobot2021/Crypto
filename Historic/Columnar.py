#!/usr/bin/env python3

"""
COLUMNAR CIPHER
A classic transposition cipher where the encryption proceeds through the columns of a square table made from the plaintext.

First, the plaintext is split into portions as long as a secret keyword, padded if necessary to reach a length that is multiple of the key. 
Then, a table is built with the text portions, entered row by row.

The encryption proceeds now by appending to the cipher the letter in the table column by column.
The order of columns follows the the order to the chacters in the secret key, sorted by their ascending value,
where the lowest char value is zero, then increasing by steps of 1.

Example of key conversion to column order:
Password: Post45
Key: [(P, 2), (o, 3), (s, 4), (t, 5), (4, 0), (5, 1)]
Columns are then encrypted in the order: [2, 3, 4, 5, 0, 1]

"""

import pandas as pd                                                                 # I have chosen pandas, numpy is a valuable alternative

# Setup values for padding the text                                             
PADDING_CHAR = '_'                                                                                                          


def to_table(text, key):
    table = pd.DataFrame(columns = range(len(key)))                                 # Create empty table, with columns from "0" to the length of the key
    while len(text) % len(key) != 0:                                                # Pad the text and the tail, to fit into the table
        text += PADDING_CHAR
    j = 0
    for i in range(0, len(text), len(key)):                                         # Split the text in chunks as long as the key length, and load them into the rows of the table
        chunk = list(text[i: i + len(key)])
        table.loc[j] = chunk
        j += 1
    return table


def to_index(key):
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
    table = to_table(text, key)                                                     # Table the text
    key = to_index(key)                                                             # Convert the key from string into sorted tuples containing the ordered values of the key chars
    enc_text = ''
    for column in key:
        enc_text += ''.join(table[column[1]])                                       # Encrypt by proceeding through each column, in the order given by the ranked key chars
    return enc_text.replace(PADDING_CHAR, '')                                       # Remove the padding chars

    
if __name__ == '__main__':
    text = input('Type your text: ')
    text = text.replace(' ', '')                                                    # Remove string spaces from the plaintext

    key = input('Type your secret key: ')
    
    # Encryption
    enc_text = columnar_encrypt(text, key)
    print(f'\nCiphertext: {enc_text}')
