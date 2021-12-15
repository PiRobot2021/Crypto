#/usr/bin/env python3
"""
PLAYFAIR CIPHER
Sometimes called the Wheatstone-Playfair cipher, or Playfair square.
The cipher relies on a key mapped in a 5x5 matrix and four rules.

First, a 5x5 matrix is filled with the keyword (removing duplicated letters), then all other letters are filled in ascending order, 
combining i/j in the same cell.

Then, the plaintext is split into chunks of 2 chars, eventually padding with a "z" at the end.
If same same letter duplicates in a cahr tuple, the second letter is replaced by "x".
Playfair does not encrypt puctuation marks and digits, so they have to be removed or left unencrypted.

Next, map each pair of letters in the 5x5 matrix 
Depending on their relative position, the encryption follows different paths.

1.) If they form a rectangle, take the opposite corners (top to bottom order) to form the cipher.
2.) If the are aligned, shift by one position (right or down), wrap to top or left if needed.

This cipher disrupts the letter and word frequencies.

"""

import pandas as pd
import string

az= {i for i in string.ascii_lowercase if i != 'j'}


def map_key(key):                                                                       
    key= key.replace('j', 'i')                                                          # The playfair square admits 25 values, so usualy "j" and "i" are combined
    key_letters= sorted(set(key))                                                       # Remove duplicate letters from the key, and sort them in ascending order
    key_letters.extend(sorted(az.difference(key_letters)))                              # attach the remaining alphabet letters, obtained by logical exclusion
    table= pd.DataFrame([key_letters[i:i+5] for i in range(0, len(key_letters), 5)])    # Load the newly ordered alphabet into a 5 x 5 matrix
    return table


def prep(text):
    text= text.replace(' ', '')                                                         # Playfair cipher does not allow spaces between words
    if len(text) % 2 != 0:                                                              # If the length of the text is odd, is padded with "z"
        text += 'z'
    result= []
    for i in range(0, len(text), 2):                                                    # The text is split in chunks of two letters
        chunk= [text[i], text[i+1]]
        if chunk[0] == chunk[1]:                                                        # If the letters in the chunk are the same, the second is replaced by "x"
            chunk[1]= 'x'
        result.append(chunk)
    return result


def find_coords(table, value):
    for i in range(len(table)):
        index= table.loc[table[i].values == value].index.values                         # Find the row at which the column value corresponds to the input value
        if index.size > 0:                                                              # When the row is found, return the coordinates
            return index[0], i


def play_fair_process(table, a, b):
    text= ''
    if a[0] == b[0]:                                                                    # If the letters of the plaintext chunk sit in the same row
        if a[1] < b[1]:                                                                 # this check guarantees that the text always shifts right
            chunk= table.loc[b[0], b[1]] + table.loc[b[0], (b[1] + 1) % len(table)]
        else:
            chunk= table.loc[a[0], a[1]] + table.loc[a[0], (a[1] + 1) % len(table)]
        text+= chunk
    elif a[1] == b[1]:                                                                  # If the letters of the plaintext chunk sit in the same column
        if a[0] < b[0]:                                                                 # this check guarantees that the text always shifts down
            chunk= table.loc[b[0], b[1]] + table.loc[(b[0] + 1) % len(table), b[1]]
        else:
            chunk= table.loc[a[0], a[1]] + table.loc[(a[0] + 1) % len(table), a[1]]
        text+= chunk
    else:
        if (a[0] < b [0] and a[1] < b[1]) or (a[0] > b[0] and a[1] > b[1]):             # If the letters form a diagonal top-left to down-right
            chunk= table.loc[a[0], b[1]] + table.loc[b[0], a[1]]
            text+= chunk
        else:                                                                           # Else the letters form a diagonal top-right to down-left
            chunk= table.loc[b[0], a[1]] + table.loc[a[0], b[1]]
            text+= chunk
    return text
        

def encrypt(text, key):
    table= map_key(key.lower())
    text= prep(text.lower())
    cipher= ''
    for i in text:
        first= find_coords(table, i[0])
        second= find_coords(table, i[1])
        cipher+= play_fair_process(table, first, second)
    return cipher
            

def main():
    text= input('Type your text: ')
    key= input('Type a password (only ascii chars): ')
    assert(key.islower() or key.isupper())                                              # Playfair accepts keywords with only letters
    assert(text.islower() or text.isupper())                                            # Playfair can only encrypt letters 
    cipher= encrypt(text, key)
    print(f'\nCipher: {cipher}')

main()
