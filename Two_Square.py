#/usr/bin/env python3
"""
TWO SQUARE CIPHER
Sometimes called Double Playfair cipher.
Instead of one 5x5 matrix, this cipher relies on two 5x5 matrixes, paired either horizontally or vertically.
Each matrix is built on an independent key, so this cipher is biult on two keys.
The keys are mapped using the same rules of Playfair: first, a 5x5 matrix is filled with the keyword (removing duplicated letters), 
then all other letters of the alphabet are filled in ascending order, combining i/j in the same cell. A variation could be to remove the "q".


Like Playfair, the plaintext is split into pairs of 2 letters.
Text of odd length is padded with a "z".
In this case, if a letter pair contains the same letter, the second letter is not replaced by "x".

The same encryption rules of Playfair apply, but the two letters are mapped in two matrixes rather than one.
The only exception is that is the letters line up on the same row or column, the pair is left unencrypted.

"""

import numpy as np
import string
import re

VARIANT= 'V' # vertical
#VARIANT= 'H' # horizontal
assert(VARIANT in ('V', 'H'))

az= {i for i in string.ascii_lowercase if i != 'j'}
#az= {i for i in string.ascii_lowercase if i != 'q'}


def print_horizontal_tables(tables):
    print('\nFirst key map:\t\t  Second key map:')
    for i in range(len(tables[0])):
        print(tables[0][i], tables[1][i])
    print()
    

def map_key(key):                                                                       
    key= key.replace('j', 'i')
    #key= key.replace('q', '')                                                          
    key_letters= sorted(set(key))                                                       
    key_letters.extend(sorted(az.difference(key_letters)))                              
    table= np.char.array(key_letters).reshape((5, 5))
    return table


def prep(text):  
    text= text.replace('j', 'i')
    #text= text.replace('q', '')    
    if len(text) % 2 != 0:                                                              
        text += 'z'
    result= []
    for i in range(0, len(text), 2):                                                   
        chunk= [text[i], text[i+1]]
        result.append(chunk)
    return result


def find_coords(table, value):
    index= np.where(table == value)
    return (index[0][0], index[1][0])


def two_square_process(tables, a, b):
    cipher= ''
    if VARIANT == 'V':                                                              # If encrypting using tables aligned vertically
        if a[1] == b[1]:
            cipher+= tables[0][a] + tables[1][b]                                    # If the letters line up vertically in the tables, add to the cipher the pair as such
        else:                                                                       # Else encrypt through a diagonal. In two_square cipher diagonals flow always top to bottom.
            cipher+= tables[0][a[0], b[1]] + tables[1][b[0], a[1]]                  # Swapping the diagonal. Add to the cipher the letters at opposite corners of the pair
    else:                                                                           # Same logic for horizontally aligned tables
        if a[0] == b[0]:                                                            # If the letters line up horizontally in the tables, add to the cipher the pair as such
            cipher+= tables[0][a] + tables[1][b]
        else:
            cipher+= tables[0][b[0], a[1]] + tables[1][a[0], b[1]]                  # Swapping the diagonal. Add to the cipher the letters at opposite corners of the pair
    return cipher
        

def encrypt(text, key1, key2):
    cipher= ''
    tables= list(map(map_key, [key1.lower(), key2.lower()]))
    text= prep(text)
    if VARIANT == 'V':
        print(f'\nFirst key map:\n{tables[0]}\n\nSecond key map:\n{tables[1]}\n')
    else:
        print_horizontal_tables(tables)
    for i in text:
        first= find_coords(tables[0], i[0])
        second= find_coords(tables[1], i[1])
        cipher+= two_square_process(tables, first, second)
    return cipher
            

def main():
    text= input('Type your text: ')
    text= re.sub('[\t\s]', '', text) 
    assert(text.islower() or text.isupper())                                        # Two_square cipher can encrypt only letters
    
    key1= input('Type a password (only ascii chars): ')
    key1= re.sub('[\t\s]', '', key1)
    assert(key1.islower() or key1.isupper())                                        # Playfair accepts keywords containing only letters
    
    key2= input('Type a password (only ascii chars): ')
    key2= re.sub('[\t\s]', '', key2)
    assert(key2.islower() or key2.isupper())                                        # Playfair accepts keywords containing only letters
    
    cipher= encrypt(text, key1, key2)
    print(f'Cipher: {cipher}')

main()
