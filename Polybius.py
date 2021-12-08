#!/usr/bin/env python3
"""
POLYBIUS CIPHER
a.k.a. Polybius square, built as a 5 by 5 grid containing the alphabet, where i and j are combined.
Each letter is represented by the two coordinates of the letter in the Polybius square.
It is a single substitution number

Usage:
to encrypt a plaintext: -e plaintext
to decrypt through a known Polybius square: -d ciphertext
"""


from sys import argv
import string
import numpy as np

az= [i for i in string.ascii_lowercase if i != 'j']                             # "j" in plaintext will be encrypted as "i"
lower_ps= np.char.array(az, unicode= True).reshape((5, 5))                      # Creating the Polybius square for letters in lower ascii


def encrypt(plaintext):
    cipher= np.empty(0, dtype= 'int')                                           # Empty array to receive the encrypted letters
    plaintext= plaintext.replace('j', 'i')                                      # Replacing all j
    for l in plaintext:
        if l in az:
            xy= np.where(lower_ps == l)                                         # Find the coordinates of the letter
            cipher= np.append(cipher, xy[0])                                    # Append the coordinates to the cipher
            cipher= np.append(cipher, xy[1])
        elif l.isdigit():       
            cipher= np.append(cipher, ' ')                                      # If digit, append a separator. I added this just to simplify the decryption.
            cipher= np.append(cipher, l)                                        # It can be better obfuscated. I keep it simple here just to learn the process.
    print(''.join(cipher.tolist()))


def decrypt(cipher):
    plaintext= ''
    cipher= list(zip(cipher[::2], cipher[1::2]))                                # Buld the coordinates
    for i in cipher:
        if i[0] == ' ':                                                         # Simply to apply the separator I added in the encryption to identify digits
            plaintext+= i[1]                                                    
        else:
            plaintext+= lower_ps[(int(i[0]), int(i[1]))]                        # Obtain the letter from the coordinates of the Polybius square
    print(plaintext)


def main():
    if argv[1] == '-e':                                                         # Encrypting with -e option
        plaintext= ' '.join(argv[i] for i in range(2, len(argv)))               # If multiple words are given, they are merged into a string
        encrypt(plaintext.lower())                           
    elif argv[1] == '-d':                                                       # Decrypting with -d option
        cipher= ' '.join(argv[i] for i in range(2, len(argv)))                  # If the ciphertext contains multiple words, they are mergeed into a string
        decrypt(cipher)                                                         
    else:
        print('To encrypt a plaintext through two integer keys: Polybius.py -e plaintext')
        print('To decrypt a ciphertext: Polybius.py -d ciphertext')

main()
