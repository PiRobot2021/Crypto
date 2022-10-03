#/usr/bin/env python3
"""
PLAYFAIR CIPHER
Sometimes called the Wheatstone-Playfair cipher, or Playfair square.
The cipher relies on a key mapped in a 5x5 matrix and four rules.

First, a 5x5 matrix is filled with a keyword (removing duplicated letters), then all other letters of the alphabet are filled in ascending order, till the matrix is completed. 
The matrix can only contain 25 letters, so "i/j" are usually combined. A variation could be to remove the "q".

Then, the plaintext is split into pairs of 2 letters, if the text length is odd is padded with a "z" at the end.
If a pair consists of the same letter, the second is replaced by "x".

Playfair does not encrypt chars other than letters, so punctiations and digits have to be removed or left unencrypted.

At last, map each pair of letters in the 5x5 matrix and begin the encryption. 
Depending on the position of the letters, the encryption follows different rules.
1.) If they form a diagonal, add to the cipher the opposite corners of the formed rectangle.
2.) If the are aligned on the same row or column, rotate the pair by one position right or down (wrap to top or left if needed),
    and add the new pair to the cipher.

This cipher disrupts the letter and word frequencies by encrypting letters by pairs rather than individually.

"""

import pandas as pd                                                                       # I decided to use pandas, for two square and four square variations I use numpy to compare the codes
import string
import random

KEY_LEN = 5
PADDING_CHAR = 'z'

az = {i for i in string.ascii_lowercase if i != 'j'}                                      # An alternative could be to remove the "q"
#az = {i for i in string.ascii_lowercase if i != 'q'}                                     

def map_key(key):                                                                       
    key_letters = sorted(set(key))                                                        # Remove duplicate letters from the key, and sort them in ascending order
    print(f'Sorted key letters: {key_letters}')
    key_letters.extend(sorted(az.difference(key_letters)))                                # attach the remaining alphabet letters, obtained by logical exclusion
    table = pd.DataFrame([key_letters[i:i + 5] for i in range(0, len(key_letters), 5)])   # Load the newly ordered alphabet into a 5 x 5 matrix
    return table


def prep(text):    
    text = text.replace('j', 'i')                                                          # The playfair square admits 25 values, here I combined "j" and "i" letters in the key
    #text = text.replace('q', '')
    if len(text) % 2 != 0:                                                                 # If the length of the text is odd, one pad char is appended
        text += PADDING_CHAR
    result = []
    for i in range(0, len(text), 2):                                                       # The text is split in chunks of two letters
        chunk = [text[i], text[i + 1]]
        if chunk[0] == chunk[1]:                                                           # If the letters in the chunk are the same, the second is replaced by "x"
            chunk[1] = 'x'
        result.append(chunk)
    return result


def find_coords(table, value):
    for i in range(len(table)):
        index = table.loc[table[i].values == value].index.values                           # Find the row at which the column value corresponds to the input value
        if index.size > 0:                                                                 # When the row is found, return the coordinates
            return index[0], i


def play_fair_process(table, a, b):
    cipher = ''
    if a[0] == b[0]:                                                                       # If the letters of the plaintext chunk sit in the same row
        rotate_down = (max(a[1], b[1]) + 1) % len(table)
        cipher += table.loc[a[0], max(a[1], b[1])] + table.loc[a[0], rotate_down]          # Add to the cipher the two letters rotated by one position downwards
    elif a[1] == b[1]:                                                                     # If the letters of the plaintext chunk sit in the same column
        rotate_right= (max(a[0], b[0]) + 1) % len(table)
        cipher += table.loc[max(a[0], b[0]), a[1]] + table.loc[rotate_right, a[1]]         # Add to the cipher the two letters rotated by one position rightwards
    else:
        if (a[0] < b [0] and a[1] < b[1]) or (a[0] > b[0] and a[1] > b[1]):                # If the letters form a diagonal top-left to down-right
            cipher += table.loc[a[0], b[1]] + table.loc[b[0], a[1]]                        # Add to the cipher the letters at the edges of the opposite diagonal top-right to down-left 
        else:                                                                              # Else the letters form a diagonal top-right to down-left
            cipher += table.loc[b[0], a[1]] + table.loc[a[0], b[1]]                        # Add to the cipher the letters at the edges of the opposite diagonal top-left to down-right
    return cipher
        

def encrypt(text, key):
    table = map_key(key)
    text = prep(text)
    cipher = ''
    print(f'Mapped key:\n{table}')
    for i in text:
        first = find_coords(table, i[0])
        second = find_coords(table, i[1])
        cipher += play_fair_process(table, first, second)
    return cipher
            

def main():
    text = input('Type your text: ')
    text = text.replace(' ', '').lower()                                                   # Playfair cipher does not allow spaces between words
    assert(text.isalpha())                                                                 # Playfair can only encrypt letters 
    
    key = random.choices(az, k=KEY_LEN)
    print(f'Random key: {key}')
    
    cipher = encrypt(text, key)
    print(f'\nCipher: {cipher}')

if __name__ == '__main__':
    main()


