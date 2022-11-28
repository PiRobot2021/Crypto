#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding, Counter


TEXT = b'Type your secret data here...'
PAD_MODE = {0:'pkcs7', 1:'iso7816', 2:'x923'}
KEY_SIZE = 16  #bytes


def ECB_mode(key, padded_text):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext


def CBC_mode(key, padded_text):
    iv = get_random_bytes(KEY_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext, iv


def CTR_mode(key, padded_text):
    nonce = get_random_bytes(8)
    ctr = Counter.new(64, prefix=nonce, initial_value=1)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext, nonce


if __name__ == '__main__':
    padded_text = Padding.pad(TEXT, KEY_SIZE, PAD_MODE[2])
    key = get_random_bytes(KEY_SIZE)
    ecb_ciphertext = ECB_mode(key, padded_text)
    cbc_ciphertext, iv = CBC_mode(key, padded_text)
    ctr_ciphertext, nonce = CTR_mode(key, padded_text)
    
