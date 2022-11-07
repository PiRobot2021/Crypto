#!/usr/bin/env python3
"""
VIGENERE CIPHER
The encryption and decryption processes proceed using a multi-alphabet square table called "tabula recta", where the text is combined with a secret key.
Such table consists of the alphabet letter rotated by one position left at each row, so to have a diagonal simmetry property.

During encryption, each letter of plaintext is set as column of such table (x coordiante), while the corresponding key letter is set as row (y coordinate).
# The letter in the table of coordiantes "x, y" is the encrypted letter of the ciphertext.
# After each letter encryption, the key rotates so that the next key letter to the right is used. The encryption process cycles through the key until the all the plaintext letters are encrypted.

# During decryption, each ciphertext letter corresponds to the x axis (columns). The column set by that letter is scrolled down until the corresponding key letter is reached.
# The plaintext letter is the y coordinate (row index) of that position.

# A variation of the Vigenere cipher is the Beaufort cipher, where encryption and decryption processes are simply switched.
"""


import string
import random
import pandas as pd
from collections import deque


KEY_LENGTH = 5

# This piece of code is required to run classic encryption and decryption functions.
# It build a Vegenere table as a pandas DataFrame
az = deque(string.ascii_lowercase)                                              # Creating a deque of the alphabet
tabula= pd.DataFrame(columns=az, index=az)                                      # Building an empty tabula
for i in string.ascii_lowercase:                                                # Filling tabula row by row
    tabula[i] = az
    az.rotate(-1)                                                               # Rotating the deque left by one at each row


# This function mimics the classic historical way of encrypting with Vigenere cipher
def encrypt_classic(key, text):
    cipher = ''
    key = list(key)                                                             # Converint the keyword into a list of characters
    for i, l in enumerate(text):
        k = key[i % len(key)]                                                   # Rotating through the key letters
        if l in string.ascii_lowercase:
            cipher += tabula.loc[l][k]                                          # Encrypting through the tabula using the plaintext letter "l" and key char "k" as coordinates
        elif l in string.ascii_uppercase:
            cipher += tabula.loc[l.lower()][k].upper()
        else:
            cipher += l
    return cipher


# This function mimics the classic historical way of decrypting with Vigenere cipher and a known key
def decrypt_classic(key, cipher):
    text = ''
    key = list(key.lower())
    for i, l in enumerate(cipher):
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


# same logic, but th ecipher process is built on arithmetic of ascii values mod 26
def encrypt(key, text):
    cipher = ''
    for i, l in enumerate(text):
        if l in string.ascii_lowercase:
            cipher += chr(((ord(l) + ord(key[i % len(key)].lower()) - 2 * ord('a')) % 26) + ord('a'))
        elif l in string.ascii_uppercase:
            cipher += chr(((ord(l.lower()) + ord(key[i % len(key)].lower()) - 2 * ord('a')) % 26) + ord('a')).upper()
        else:
            cipher += l
    return cipher

def decrypt(key, cipher):
    text = ''
    for i, l in enumerate(cipher):
        if l in string.ascii_lowercase:
            text += chr(((ord(l) - ord(key[i % len(key)].lower())) % 26) + ord('a'))
        elif l in string.ascii_uppercase:
            text += chr(((ord(l.lower()) - ord(key[i % len(key)].lower())) % 26) + ord('a')).upper()
        else:
            text += l
    return text


def main():
    plain = input('Type your text: ')
    key = ''.join(random.choices(string.ascii_lowercase, k=KEY_LENGTH))                # This Vigenre variation using a random key is also called "running key cipher"
    print(f'Random key: {key}')
    #print(f'Vigenere table:\n{tabula}')
    
    # Encryption
    cipher = encrypt_classic(key, plain)                               
    print(f'\nCipher: {cipher}')
    cipher = encrypt(key, plain)
    print(f'Cipher: {cipher}')

    # Decryption
    plain = decrypt_classic(key, cipher)
    print(f'Plaintext: {plain}')
    plain = decrypt(key, cipher)
    print(f'Plaintext: {plain}')

    

if __name__ == '__main__':
    main()
