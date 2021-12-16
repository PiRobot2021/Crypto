#/usr/bin/env python3
"""
FOUR SQUARE CIPHER

Another variation of the Playfair cipher, using 4 5x5 matrixes, organized in a square:

1   2
3   4

The order of the letters may vary in each matrix, according to keys mapped exactly as in the Playfair square rule.
Though variations using 4 keys are possible, normally only the alphabets in the matrixes 2 and 3 are transposed.

Like Playfair, the plaintext is split into pairs of 2 letters, and if the length of the text is odd, is padded with a "z" at the end.
Like the two_square cipher, it is allowed to have pairs contains the same letter.

The encyrption proceeds by mapping the letter pairs on the matrixes 1 and 4, 
then add to the cipher the corresponding letters in the matrixes 2 and 3.
In this cipher the letters in the pairs are always in a diagonal relationship.

"""

import numpy as np
import string
import re


az= {i for i in string.ascii_lowercase if i != 'j'}
#az= {i for i in string.ascii_lowercase if i != 'q'}


def print_tables(tables):
    print('\nFirst key map:\t\t  Second key map:')
    for i in range(len(tables[0])):
        print(tables[0][i], tables[1][i])
    print('\nThird key map:\t\t  Fourth key map:')
    for i in range(len(tables[0])):
        print(tables[2][i], tables[3][i])
    print()
   

def map_key(key):                                                                       
    key= re.sub('[\t\s]', '', key)
    key= key.replace('j', 'i')
    #key= key.replace('q', '')                                                          
    key_letters= sorted(set(key))                                                       
    key_letters.extend(sorted(set(az).difference(key_letters)))                              
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


def four_square_process(tables, a, b):
    return tables[1][a[0], b[1]] + tables[3][b[0], a[1]]
        

def encrypt(text, key1, key2):
    cipher= ''
    tables= list(map(map_key, [key1, string.ascii_lowercase, key2, string.ascii_lowercase]))
    text= prep(text)
    print_tables(tables)
    for i in text:
        first_letters= find_coords(tables[0], i[0])
        second_letters= find_coords(tables[3], i[1])
        cipher+= four_square_process(tables, first_letters, second_letters)
    return cipher
            

def main():
    text= input('Type your text: ')
    text= re.sub('[\t\s]', '', text.lower()) 
    assert(text.isalpha())
    
    key1= input('Type a password (only ascii chars): ')
    assert(key1.isalpha() or not key1)                                              
    key2= input('Type a password (only ascii chars): ')
    assert(key2.isalpha() or not key2)                                            
    
    cipher= encrypt(text, key1, key2)
    print(f'Cipher: {cipher}')

main()
