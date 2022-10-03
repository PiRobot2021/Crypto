#!/usr/bin/env python3

"""
RAIL FENCE CIPHER
I classic transposition cipher, where the plaintext is split in two lines of same length,
and the encryption proceed alternating through the letters in the two lines.
    
"""

PADDING_CHAR = '_'

def encrypt(text):
    if len(text) % 2 != 0:
        text += PADDING_CHAR
    chunk_one = text[:len(text)//2]
    chunk_two = text[len(text)//2:]
    cipher = ''
    for i in range(len(text) // 2):
        cipher += chunk_one[i] + chunk_two[i]
    return cipher

    
def main():
    text = input('Type your text: ')
    
    # Encryption
    cipher = encrypt(text)
    print(f'\nCipher: {cipher}')

if __name__ == '__main__':
    main()
