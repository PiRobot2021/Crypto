#!/usr/bin/env python3

"""
RAIL FENCE CIPHER
I classic transposition cipher. The encryption process proceeds by dividing the plaintext into rails, through alternating diagonals.
e.g. "attack at dawn!" encrypted using 4 rail cipher would lead to:
Rail 1:    a.......a.....n.
Rail 2:    .t..... .t...w.!
Rail 3:    ..a..k.... .a...
Rail 4:    ...c.......d....
The ciphertext is obtained by concatenating the rail strings "aant tw!ak acd". 
The decryption follows in the inverse order, diving the ciphertext into string sections of appropriate length (see execution below),
then rebuilding the plaintext by concatenating the letter in the proper diagonal order.
"""

from collections import deque


N = 5               # Number of rails. It must be lower than the length of the text.
assert(N > 1)


def encrypt(plain, N):
    L = len(plain)
    x = 0
    find_diagonals = N + ((N - 1) * x)
    while find_diagonals < L:
            x += 1
            find_diagonals = N + ((N - 1) * x)
     
    if N >= len(plain) or x < 2:                                # The cipher should proceed at least through 2 diagonals and N should be lower than L
        print('Too many rails, please chose a lower N value')
        return None
    
    rails = []                                                  # Create an empty list of rails.
    for i in range(N):                                          # Each rail is initialized as an empty list
        rails.append(list())
        
    plain = deque(plain)
    while True:
        try:
            if N > 2:                                           # The encryption process is programmed differently is using more than 2 rails
                for i in rails:                                 # First append the plantext top down
                    i.append(plain.popleft())                   
                for i in range(len(rails) - 2, 0, -1):          # Then append the plaintext bottom up
                    rails[i].append(plain.popleft())
            else:                                               # If only using 2 rails, encrypt by simple alternation.
                for i in rails:
                    i.append(plain.popleft())
        except IndexError:                                      # When the deque containing the plaintext is empty, an IndexError occurs. We can collect the ciphertext 
            return ''.join([''.join(i) for i in rails])


def describe_ciphertext(L, N, x, y, K):
    print(f'Length: {L}\nRails: {N}\nDiagonals: {x}\nOptional end pads: {y}\nCycle key K: {K}\n')


def decrypt(enc, N):
    L = len(enc)
    x = 0
    find_diagonals = N + ((N - 1) * x)
    while find_diagonals <= L:
            x += 1
            find_diagonals = N + ((N - 1) * x)
    y = find_diagonals - L

    if N >= len(enc) or x < 2:
        print('Too many rails, please chose a lower N value')
        return None
    
    K = L // (2 * (N - 1))                                      # The ciphertext is divided into sections according to a K value that sets the length of the first and last rails
    describe_ciphertext(L, N, x, y, K)
    
    rails = []
    for i in range(N):
        rails.append(deque())

    plain = []    
    if N > 2:                                                   # Decrypting for more than 2 rails is more complex and programmed differently
            # Default offsets to zero
            offsets = [0 for i in rails]                        # If L % (2 * (N - 1)) == 0, the decryption proceeds automatically, we can neglect the offsets of all rail length
            
            # Manual offset adjustments                         # If L % (2 * (N - 1)) != 0, the lengths of the rails may need manual adjustments to obtain the plaintext
            #offsets[1] = -1
            #offsets[2] = -1
            #offsets[3] = 0
            #offsets[4] = 2
            #offsets[5] = 0
            #...

            rails[0].extend(list(enc[:K+1]))                    # Obtain the first rail, based on K value
            step = (L - 2 * (K + 1)) // (N - 2)                 # Set the step to calculate the lenghts of the intermediate rails
            start = K + 1                                       # Initialize the start of the second rail section
            stop = K + 1 + step + 1                             # Initialize the stop of the second rail section
                    
            for i in range(1, len(rails)-1):                    # Build all the intermediate rails
                rails[i].extend(list(enc[start + offsets[i-1]:stop + offsets[i]]))
                start = stop
                stop += step
                
            rails[len(rails)-1].extend(list(enc[start + offsets[len(rails)-2]:]))       # Build the last rail         

            for i, j in enumerate(rails):                       # This print helps the manual offset adjustments, the intermediate rails should target length 2*K
                print(f'Rail {i}: {len(j)} {j}')

            while True:
                try:                                            # This is the same inverse process of encryption
                    for i in rails:
                        plain.append(i.popleft())
                    for i in range(len(rails) - 2, 0, -1):
                        plain.append(rails[i].popleft())
                except IndexError:
                    return ''.join([i for i in plain])          # When the rails are empty, an IndexError occurs. We can collect the plaintext 
    else:                                                       # This condition is used to decrypt a 2 rail cipher instead
        rails[0].extend(list(enc[:K]))
        rails[len(rails)-1].extend(list(enc[-1*K:]))   
        while True:
            try:
                for i in rails:
                    plain.append(i.popleft())
            except IndexError:
                return ''.join(plain)
        
        
def main():
    text = input('Type your text: ')
    
    # Encryption
    cipher = encrypt(text, N)
    print(f'\nCiphertext: {cipher}')

    # Decryption
    text = decrypt(cipher, N)
    print(f'\nPlaintext: {text}')


if __name__ == '__main__':
    main()

