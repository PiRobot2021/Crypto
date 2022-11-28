#!/usr/bin/env python3
"""
VIGENERE CIPHER
The encryption and decryption proceed using a multi-alphabet square table called "tabula recta", where the text is combined with a secret key.
Such table consists of the alphabet letter rotated by one position left at each row, so to have a diagonal simmetry property.

During encryption, each letter of plaintext is set as column of such table (x coordiante), while the corresponding key letter is set as row (y coordinate).
# The letter in the table of coordiantes "x, y" is the encrypted letter of the ciphertext.
# After each letter encryption, the key rotates so that the next key letter to the right is used. The encryption process cycles through the key until the all the plaintext letters are encrypted.

# During decryption, each ciphertext letter corresponds to the x axis (columns). The column set by that letter is scrolled down until the corresponding key letter is reached.
# The plaintext letter is the y coordinate (row index) of that position.

# A variation of the Vigenere cipher is the Beaufort cipher, where encryption and decryption processes are inverted.
"""


import string
import secrets
import pandas as pd
from collections import deque


KEY_LENGTH = 5

# This piece of code is required to run classic encryption and decryption functions.
# It builds a Vegenere table as a pandas DataFrame using alphabet deques
az = deque(string.ascii_lowercase)                                              # Creating a deque of the alphabet
tabula= pd.DataFrame(columns=az, index=az)                                      # Building an empty tabula
for i in string.ascii_lowercase:                                                # Filling tabula row by row
    tabula[i] = az
    az.rotate(-1)                                                               # Rotating the deque left by one at each row


# This function mimics the classic encryption process of Vigenere cipher
def encrypt_classic(key, text):
    enc_text = ''
    key = list(key)                                                             
    for i, l in enumerate(text):
        k = key[i % len(key)]                                                   # Rotate through the key letters
        if l in string.ascii_lowercase:
            enc_text += tabula.loc[l][k]                                        # The plaintext letter "l" and the key letter "k" as the coordinates of the ciphertext
        elif l in string.ascii_uppercase:
            enc_text += tabula.loc[l.lower()][k].upper()
        else:
            enc_text += l
    return enc_text


# This function mimics the classic decryption process of Vigenere cipher, with a known key
def decrypt_classic(key, enc_text):
    text = ''
    key = list(key.lower())
    for i, l in enumerate(enc_text):
        k = key[i % len(key)]
        if l in string.ascii_lowercase:
            c = tabula[k].where(tabula[k] == l).dropna()                                # Decrypting by searching at which row index the column of the key "k" has the value of the cipher "l"
            text += c.index[0]
        elif l in string.ascii_uppercase:
            c = tabula[k].where(tabula[k] == l.lower()).dropna()                        # Decrypting by searching at which row index the column of the key "k" has the value of the cipher "l"
            text += c.index[0].upper()
        else:
            text += l
    return text


# Instead of proceeding through the Vigenere table, this function does arithmetic from ascii values mod 26
def encrypt(key, text):
    enc_text = ''
    k = 0
    for i, l in enumerate(text):
        if l in string.ascii_lowercase:
            enc_text += chr(((ord(l) + ord(key[k % len(key)].lower()) - 2 * ord('a')) % 26) + ord('a'))
            k += 1
        elif l in string.ascii_uppercase:
            enc_text += chr(((ord(l.lower()) + ord(key[k % len(key)].lower()) - 2 * ord('a')) % 26) + ord('a')).upper()
            k += 1
        else:
            enc_text += l
    return enc_text


def decrypt(key, enc_text):
    text = ''
    k = 0
    for i, l in enumerate(enc_text):
        if l in string.ascii_lowercase:
            text += chr(((ord(l) - ord(key[k % len(key)].lower())) % 26) + ord('a'))
            k += 1
        elif l in string.ascii_uppercase:
            text += chr(((ord(l.lower()) - ord(key[k % len(key)].lower())) % 26) + ord('a')).upper()
            k += 1
        else:
            text += l
    return text


if __name__ == '__main__':
    text = input('Type your text: ')
    key = ''.join([secrets.choice(string.ascii_lowercase) for i in range(KEY_LENGTH)])                # This Vigenre variation using a random key is also called "running key cipher"
    print(f'Random key: {key}')
    #print(f'Vigenere table:\n{tabula}')
    
    # Encryption
    enc_text = encrypt_classic(key, text)                               
    print(f'\nCiphertext: {enc_text}')
    enc_text = encrypt(key, text)
    print(f'Ciphertext: {enc_text}')

    # Decryption
    text = decrypt_classic(key, enc_text)
    print(f'Plaintext: {text}')
    text = decrypt(key, enc_text)
    print(f'Plaintext: {text}')

