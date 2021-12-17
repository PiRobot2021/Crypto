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
import random
import numpy as np
import pandas as pd

LEN_KEY= 5
PADDING_CHAR= '_'       

def create_square():
    values= [i for i in string.digits + string.ascii_lowercase]
    random.shuffle(values)
    return np.char.asarray(values).reshape(6, 6)


def find_coords(square, letter):
    ADFGVX= dict(zip([i for i in range(6)], list('ADFGVX')))
    a= np.where(square == letter)
    return ADFGVX[a[0][0]] + ADFGVX[a[1][0]]


def ADFGVX(text):
    square= create_square()
    print(f'\nADFGVX random square:\n{square}')
    cipher= ''
    for i in text:
        cipher+= find_coords(square, i)
    return cipher
                                                                                                

def to_table(text, key):
    table= pd.DataFrame(columns= [i for i in range(len(key))])                      # Create empty table, with columns from "0" to the length of the key
    while len(text) % len(key) != 0:                                                # Pad the text and the tail, to fit into the table
        text+= PADDING_CHAR
    j= 0
    for i in range(0, len(text), len(key)):                                         # Split the text in chunks as long as the key length, and load them into the rows of the table
        chunk= [i for i in text[i: i + len(key)]]
        table.loc[j]= chunk
        j+= 1
    return table


def to_index(key):
    sorted_key_chars= sorted(key)
    ascending_int= [i for i in range(len(key))]
    ordered_key= list(zip(sorted_key_chars, ascending_int))                         # list of tuples containing sorted key chars and growing int values by steps of 1
    result= []
    for x in key:
        for y in ordered_key:
            if y[0] == x:
                result.append(y)
                ordered_key.remove(y)                                               # Removing the tuple from the ordered_key to avoid duplications in the next key values
                break                                                               # Once value is found, stop rotating through the ordered_keys
    return result


def columnar_encrypt(text, key):
    print(f'\nIntermediate cipher: {text}')
    table= to_table(text, key)                                                      # Table the text
    print(f'\nSquared intermediate cipher:\n{table}')
    key = to_index(key)                                                             # Convert the key from string into sorted tuples containing the ordered values of the key chars
    cipher= ''
    for column in key:
        cipher+= ''.join(table[column[1]])                                          # Encrypt by proceeding through each column, in the order given by the ranked key chars
    return cipher.replace(PADDING_CHAR, '')                                         # Remove the padding chars
    
    
def encrypt(text, key):
    intermediate_cipher= ADFGVX(text)
    cipher= columnar_encrypt(intermediate_cipher, key)
    return cipher


def main():
    text= input('Type your text (only letters, digits and spaces): ')
    text= text.replace(' ', '').lower()
    assert(text.isalnum())

    key= random.choices(string.ascii_lowercase, k= LEN_KEY)
    print(f'Random key: {key}')
    
    cipher= encrypt(text, key)
    print(f'\nCipher: {cipher}')

main()
