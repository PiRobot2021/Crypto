#/usr/bin/env python3
"""
TWO SQUARE CIPHER
Sometimes called Double Playfair cipher.
Instead of one 5x5 matrix, this cipher relies on two 5x5 matrixes, paired either horizontally or vertically.
Each matrix is built on an independent key, so this cipher requires two keywords.
The keys are mapped using the same rules of Playfair: first, a 5x5 matrix is filled with the keyword (removing duplicated letters), 
then all other letters of the alphabet are filled in ascending order, combining i/j in the same cell. A variation could be to remove the "q".


Like Playfair, the plaintext is split into pairs of 2 letters, and if the length of the text is odd length, the end is padded with a "z".
In this case, it is allowed to have pairs contains the same letter.

The same encryption rules of Playfair apply, but the first letter is mapped in the first square, while the other letter in the second square.
In this way the rectangles constructed by the positions of the letters stretch between the two matrixes.
Additionally, if the letters line up on the same row or column between the two matrixes, the pair is added to the cipher as such (not transposed).

"""

import numpy as np
import string
import random

VARIANT= 'V' # vertical                                                             # The Playfair squares can be aligned vertically or horizontally      
#VARIANT= 'H' # horizontal
assert(VARIANT in ('V', 'H'))

LEN_KEYS= 5

az= {i for i in string.ascii_lowercase if i != 'j'}                                 # To build a square, one letter of the alphabet is removed, normally "j" or "q" 
#az= {i for i in string.ascii_lowercase if i != 'q'}


def print_horizontal_tables(tables):
    print('\nFirst key map:\t\t  Second key map:')
    for i in range(len(tables[0])):
        print(tables[0][i], tables[1][i])
    print()
    

def map_key(key):                                                                                                                               
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
    index= np.where(table == value)                                                 # numpy has a concise way to find coordinates of a value
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
    tables= list(map(map_key, [key1, key2]))
    text= prep(text)
    if VARIANT == 'V':
        print('\nUsing vertical variation')
        print(f'\nFirst key map:\n{tables[0]}\n\nSecond key map:\n{tables[1]}\n')
    else:
        print('\nUsing horizontal variation')
        print_horizontal_tables(tables)
    for i in text:
        first= find_coords(tables[0], i[0])
        second= find_coords(tables[1], i[1])
        cipher+= two_square_process(tables, first, second)
    return cipher
            

def main():
    text= input('Type your text: ')
    text= text.replace(' ', '').lower() 
    assert(text.isalpha())                                                          # Two_square cipher can encrypt only letters
    
    key1= ''.join(random.choices(list(az), k= LEN_KEYS))                            # Generate random letters with defined length
    print(f'First random key: {key1}')

    key2= ''.join(random.choices(list(az), k= LEN_KEYS))
    print(f'Second random key: {key2}')
    
    cipher= encrypt(text, key1, key2)
    print(f'Cipher: {cipher}')

main()
