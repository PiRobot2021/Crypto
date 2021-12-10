#!/usr/bin/env python3

"""
GEOMETRIC SHAPE CIPHER
A transposition cipher where the sender splits the text in rows, 
plots it in a square format completing the square using a padding character,
and then maps a path over it until all the letters are covered, to create the ciphertext.

The receiver can decrypt the cipher following the reverse path.

This is sometimes called "route cipher".

"""

import math
import random
import pandas as pd

RANDOM_PADDING= False
REMOVE_PADDING= True


def squaring(text):
    text= text.replace(' ', '')
    side= math.sqrt(len(text))
    if not side.is_integer():
        side= int(side) + 1
        while len(text) < pow(side, 2):
            if RANDOM_PADDING:
                index= random.randint(0, len(text))
                text= text[:index] + '_' + text[index:]
            else:
                text+= '_'
    else:
        side= int(side)
    text= [i for i in text]
    chunks= []
    for i in range(len(text[::side])):
        chunks.append(text[side * i : side * i + side])
    table= pd.DataFrame(columns=[i for i in range(side)])
    for i in range(side):
        table.loc[i]= chunks[i]
    return table


def encrypt_snake(text):
    cipher= ''
    table= squaring(text)
    for y in range(len(table)):
        if y % 2 == 0:
            for x in range(len(table)):
                cipher+= table.loc[x, y]
        else:
            for x in range(len(table) - 1, -1, -1):
                cipher+= table.loc[x, y]
    if REMOVE_PADDING:
        return cipher.replace('_', '')
    else:
        return cipher


def encrypt_diagonal(text):
    cipher= ''
    table= squaring(text)
    for x in range(len(table) - 1, -1, -1):
        y= 0
        for i in range(x, len(table)):
            cipher+= table.loc[i, y]
            y+= 1
    for y in range(1, len(table)):
        x= 0
        for i in range(y, len(table)):
            cipher+= table.loc[x, i]
            x+= 1
    if REMOVE_PADDING:
        return cipher.replace('_', '')
    else:
        return cipher
            
    
def main():
    text= input('Type your text: ')
    
    # Encryption
    cipher_snake= encrypt_snake(text)
    print(f'Encrypted through snake path: {cipher_snake}')
    cipher_diagonal= encrypt_diagonal(text)
    print(f'Encrypted through diagonal path: {cipher_diagonal}')    


main()
