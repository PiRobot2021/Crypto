#!/usr/bin/env python3
"""
MULTI-ALPHABET SUBSTITUTION CIPHER

Like a Cesar cipher, with an additional arbitrary shift of letters to obfuscate frequency analysis.
A secret key is provided together with the plaintext and the two are overlapped.
Each letter of the plaintext rotates by the corresponding digit in the key. 
When the key reaches the end, it starts again from the first digit, until all the plaintext is encrypted.
This way wach letter rotates independently from the others, preventing frequency analysis.
"""



import string

az= [i for i in string.ascii_lowercase]                             # Create a list of letters in lower ascii 
AZ= [i for i in string.ascii_uppercase]                             # Create a list of letters in upper ascii


def encrypt(key, plaintext):
    key= [int(i) for i in key]                                      # Split the input key into a list of digits
    cipher= ''
    for i, l in enumerate(plaintext):
        key_rot= key[i % len(key)]                                  # Apply key rotation syncronized with the index "i" of the letter in the plaintext
        if l in az:
            cipher+= az[(i + key_rot) % len(az)]                    # Apply the key rotation to the letter in the alphabet (lower ascii)
        elif l in AZ:
            cipher+= AZ[(i + key_rot) % len(AZ)]                    # Apply the key rotation to the letter in the alphabet (upper ascii)
        else:
            cipher+= l                                              # Leave all the other characters (digits, punctuations, etc.) untouched
    return cipher
    
    
def decrypt(cipher):
    print('Work in progress')


def main():
    # Encryption
    text= input('Type your text: ')
    key= input('Type a numeric key: ')
    cipher= encrypt(key, text)
    print(f'{cipher}\n')
    
    # Decryption
    #decrypt(cipher)

main()
