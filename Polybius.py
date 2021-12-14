#!/usr/bin/env python3
"""
POLYBIUS CIPHER
a.k.a. Polybius square, built as a 5 by 5 grid containing the alphabet, where i and j are combined.
Each letter is represented by the two coordinates of the letter in the Polybius square.
It is a single substitution number
"""


import string
import numpy as np

az= [i for i in string.ascii_lowercase if i != 'j']                             # "j" in plaintext will be encrypted as "i"
lower_ps= np.char.array(az, unicode= True).reshape((5, 5))                      # Creating the Polybius square for letters in lower ascii


def encrypt(text):
    cipher= np.empty(0, dtype= 'int')                                           # Empty array to receive the encrypted letters
    text= text.replace('j', 'i')                                                # Replacing all j
    for l in text:
        if l in az:
            xy= np.where(lower_ps == l)                                         # Find the coordinates of the letter
            cipher= np.append(cipher, xy[0])                                    # Append the coordinates to the cipher
            cipher= np.append(cipher, xy[1])
        elif l.isdigit():       
            cipher= np.append(cipher, ' ')                                      # If digit, append a separator. I added this just to simplify the decryption.
            cipher= np.append(cipher, l)                                        # It can be better obfuscated. I keep it simple here just to learn the process.
    return cipher


def decrypt(cipher):
    text= ''
    cipher= list(zip(cipher[::2], cipher[1::2]))                                # Buld the coordinates
    for i in cipher:
        if i[0] == ' ':                                                         # Simply to apply the separator I added in the encryption to identify digits
            text+= i[1]                                                    
        else:
            text+= lower_ps[(int(i[0]), int(i[1]))]                             # Obtain the letter from the coordinates of the Polybius square
    print(text)


def main():
    # Encryption
    text= input('Type your text: ')
    cipher= encrypt(text.lower())                           
    print(f'\nCipher: {cipher}\n')
    
    # Decryption
    i= input('Do you wnat to try decrypting? [y/n]: ')
    if i == 'y':
        decrypt(cipher)                                                         

main()
