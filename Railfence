#!/usr/bin/env python3

"""
RAIL FENCE CIPHER
I classic transposition cipher, where the plaintext is split in two chunks,
and the encryption proceed alternately between the letters of the two.
    
"""

PADDING_CHAR= '_'


def encrypt(text):
    if len(text) % 2 != 0:
        text+= PADDING_CHAR
    chunk_one= text[:len(text)//2]
    chunk_two= text[len(text)//2:]
    cipher= ''
    for i in range(len(text) // 2):
        cipher+= chunk_one[i] + chunk_two[i]
    return cipher

    
def main():
    text= input('Type your text: ')
    
    # Encryption
    cipher= encrypt(text)
    print(f'Encrypted: {cipher}')

main()
