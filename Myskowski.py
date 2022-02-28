#!/usr/bin/env python3

"""
MYSKOWSKI COLUMNAR CIPHER
A variation of the columnar transposition cipher.
Also in this case, the text is first split in chunks as long as the key, and the same padding rules apply.

For the encryption, the order of columns still follows the the order to the letters in the secret key, sorted by their values,
but if a letter is repeated in the key, the encryption proceeds row by row between the columns containing the repeated letter.

Example:
Password: feed44
Converted key: [('f', 5), ('e', 3), ('e', 4), ('d', 2), ('4', 0), ('4', 1)]
Column order: 5, row by row between colums 3 and 4, 2, row by row between columns 0 and 1    
"""

import pandas as pd
import random
import string

PADDING_CHAR = '_'                                                                                                          
KEY_LEN = 5

def to_table(text, key):
    table = pd.DataFrame(columns = range(len(key)))                                 # Create empty table, with columns from "0" to the length of the key
    while len(text) % len(key) != 0:                                                # Pad the text and the tail, to fit into the table
        text += PADDING_CHAR
    j = 0
    for i in range(0, len(text), len(key)):                                         # Split the text in chunks as long as the key length, and load them into the rows of the table
        chunk = [i for i in text[i: i + len(key)]]
        table.loc[j] = chunk
        j += 1
    return table


def to_index(key):
    sorted_key_chars = sorted(key)
    ascending_int = range(len(key))
    ordered_key = list(zip(sorted_key_chars, ascending_int))                        # List of tuples containing sorted key chars and growing int values by steps of 1
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
    indexed_key = to_index(key)                                                     # Convert the key from string into sorted tuples containing the key chars and their ascending int values
    print(f'Indexed key: {indexed_key}')
    print(f'Columnar table:\n{table}')
    cipher = ''
    while indexed_key:                                                              # To manage duplicates, I decided to remove items from the ordered key once the cipher processed through it
        for idx in indexed_key:
            if key.count(idx[0]) == 1:                                              # If the item in the indexed_key is unique, simply encrypt the column                
                cipher += ''.join(table[idx[1]])                                 
                indexed_key.remove(idx)
            else:                                                                   # If the item in the indexed_key is not unique
                duplicates = [val for val in indexed_key if key.count(val[0]) > 1]  # Find the subgroup of duplicates
                i = 0
                while i < len(table.index):                                         # Rotate the table through the duplicates, encrypt the cipher row by row
                    for _, v in duplicates:
                        cipher += ''.join(table.loc[i, v])
                    i += 1
                for r in duplicates:                                                # Once the cipher proceeded through them, remove the items from the indexed_key
                    indexed_key.remove(r)
                
    return cipher.replace(PADDING_CHAR, '')                                         # Remove the padding chars before returning the result
    
def main():
    text = input('Type your text: ')
    text = text.replace(' ', '') 
    assert(text.isalpha())
    
    key = ''.join(random.choices(string.digits + string.ascii_letters, k = KEY_LEN))
    print(f'Random key: {key}')
    
    # Encryption
    cipher = columnar_encrypt(text, key)
    print(f'\nCipher: {cipher}')

if __name__ == '__main__':
    main()
