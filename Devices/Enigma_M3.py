#/usr/bin/env python3
"""
ENIGMA MODEL M3 KRIEGSMARINE
Launched in 1940, part of a family of rotor based cipher machines.
I found well detailed descritpions in these links, and used them to build my code.

Electrical and mechanical overview: https://www.youtube.com/watch?v=ybkkiGtJmkM
Rotor encoding steps: https://www.youtube.com/watch?v=UKbP3Rjxhy0
Simulator: https://www.101computing.net/enigma-machine-emulator/


THE SETTINGS
The initial daily setup of the devices was written in a military "code book". An Enigma code book would have one page per month. 
The page would include all the settings for each day of the month with the first day of the month at the bottom of the page so that once used, 
a setting could be torn off the page. Setting example:
30                 Day of the month
IV II III          Rotor numbers and positions (left - middle - right)
1 2 3 (or B C D)   Ring setting, applying an additional shift to the wired rings in the rotor
DW AO QT           Plugboard switches (in this examples D to W, A to O and Q to T are active)
A F J              Initial position of the rotors
"""

import random
from collections import deque
from string import ascii_uppercase as AZ
from copy import copy

#            -> ABCDEFGHIJKLMNOPQRSTUVWXYZ <-
INNER_RING= {1:'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
             2:'AJDKSIRUXBLHWTMCQGZNPYFVOE',
             3:'BDFHJLCPRTXVZNYEIWGAKMUSQO',
             4:'ESOVPZJAYQUIRHXLNFTGKDCMWB',
             5:'VZBRGITYUPSDNHLXAWMJQOFECK',
             6:'JPGVOUMFYQBENHZRDKASXLICTW',
             7:'NZJHGRCXMYSWBOUFAIVLPEKQDT',
             8:'FKQHTLXOCBJSPDZRAMEWNIUYGV'}

# The letters in the reflector are mirrored pairs (e.g. A -> Y, so Y -> A):
#                 -> ABCDEFGHIJKLMNOPQRSTUVWXYZ <-
REFLECTOR= {'UKW_B':'YRUHQSLDPXNGOKMIEBFZCWVJAT',		
            'UKW_C':'FVPJIAOYEDRZXWGCTKUQSBNMHL'}

TURN_NOTCH= {1:'Q',        # If rotor steps from Q to R, the next rotor is advanced
             2:'E',	       # If rotor steps from E to F, the next rotor is advanced
             3:'V',	       # If rotor steps from V to W, the next rotor is advanced
             4:'J',	       # If rotor steps from J to K, the next rotor is advanced
             5:'Z',	       # If rotor steps from Z to A, the next rotor is advanced
             6:['Z', 'M'], # If rotor steps from Z to A, or from M to N the next rotor is advanced
             7:['Z', 'M'], # If rotor steps from Z to A, or from M to N the next rotor is advanced
             8:['Z', 'M']} # If rotor steps from Z to A, or from M to N the next rotor is advanced

ROTOR_NAME= {1:'I',
             2:'II', 
             3:'III',
             4:'IV',
             5:'V',
             6:'VI',
             7:'VII',
             8:'VIII'}

MANUAL_SETUP= False
DEBUG= False

def setup():
    if MANUAL_SETUP:
        rotor= (1, 2, 3)
        switches= [('A', 'B')]                                                            
        start= ('A', 'D', 'U')
        ring_setting= (0, 0, 0)
        reflector= 'UKW_B'
    else:
        rotor= tuple(random.sample(list(range(1, 9)), k= 3))
        ring_setting= tuple(random.choices(list(range(26)), k= 3))
        start= tuple(random.choices(AZ, k= 3))
        reflector= ''.join(random.choices(list(REFLECTOR.keys()), k= 1))
        
        switches= []
        first_letters= random.sample(AZ, k= 10)
        second_letters= copy(AZ)
        for i in first_letters:
            j= random.sample([n for n in second_letters if n != i], k= 1)[0]
            switches.append((i, j))
            second_letters= second_letters.replace(f'{j}', '')
            
    print(f'Rotors: {ROTOR_NAME[rotor[0]]}, {ROTOR_NAME[rotor[1]]}, {ROTOR_NAME[rotor[2]]}')
    print(f'Ring settings: {AZ[ring_setting[0]]}, {AZ[ring_setting[1]]}, {AZ[ring_setting[2]]}')
    print(f'Start positions: {start[0]}, {start[1]}, {start[2]}')
    print(f'Reflector type: {reflector}')
    print(f'Plugboard switches: {switches}\n')
    return rotor, ring_setting, start, reflector, switches


def set_rotors(start, rotor):
    ring_left= [deque(AZ), deque(INNER_RING[rotor[0]])]
    offset= -1 * AZ.index(start[0])
    ring_left[0].rotate(offset)
    ring_left[1].rotate(offset)
    
    ring_centre= [deque(AZ), deque(INNER_RING[rotor[1]])]
    offset= -1 * AZ.index(start[1])
    ring_centre[0].rotate(offset)
    ring_centre[1].rotate(offset)
    
    ring_right= [deque(AZ), deque(INNER_RING[rotor[2]])]
    offset= -1 * AZ.index(start[2])
    ring_right[0].rotate(offset)
    ring_right[1].rotate(offset)
    
    return ring_left, ring_centre, ring_right
    

def step_rotors(ring_left, ring_centre, ring_right, rotor):
    if ring_centre[0][0] in TURN_NOTCH[rotor[1]]:
            ring_centre[0].rotate(-1)
            ring_centre[1].rotate(-1)
            ring_left[0].rotate(-1)
            ring_left[1].rotate(-1)
    if ring_right[0][0] in TURN_NOTCH[rotor[2]]:
        ring_centre[0].rotate(-1)
        ring_centre[1].rotate(-1)           
    ring_right[0].rotate(-1)
    ring_right[1].rotate(-1)
    return ring_left, ring_centre, ring_right


def plugboard(letter, switches):
    for i, j in switches:
        if letter == i:
            return j
        elif letter == j:
            return i
    return letter


def Cesar(alphabets, letter, from_offset, to_offset):
    from_alphabet= copy(alphabets[0])
    from_alphabet.rotate(from_offset)

    to_alphabet= copy(alphabets[1])
    to_alphabet.rotate(to_offset)

    rot_tab= letter.maketrans(''.join(from_alphabet), ''.join(to_alphabet))                   
    return letter.translate(rot_tab)

   
def Enigma_process(text):
    rotors, ring_setting, start_positions, reflector_type, switches= setup()
    ring_left, ring_centre, ring_right= set_rotors(start_positions, rotors)
    alphabet= deque(AZ)
    
    cipher= ''    
    for i in text:    
        ring_left, ring_centre, ring_right= step_rotors(ring_left, ring_centre, ring_right, rotors)
        
        switched_letter_forward= plugboard(i, switches)
        
        rotor_right_forward= Cesar([alphabet, ring_right[1]], switched_letter_forward, 0, ring_setting[2])
        rotor_centre_forward= Cesar([ring_right[0], ring_centre[1]], rotor_right_forward, ring_setting[2], ring_setting[1])
        rotor_left_forward= Cesar([ring_centre[0], ring_left[1]], rotor_centre_forward, ring_setting[1], ring_setting[0])

        reflector_in= Cesar([ring_left[0], alphabet], rotor_left_forward, ring_setting[0], 0)
        reflector_out= Cesar([deque(REFLECTOR[reflector_type]), ring_left[0]], reflector_in, 0, ring_setting[0])
        
        rotor_left_backward= Cesar([ring_left[1], ring_centre[0]], reflector_out, ring_setting[0], ring_setting[1])
        rotor_centre_backward= Cesar([ring_centre[1], ring_right[0]], rotor_left_backward, ring_setting[1], ring_setting[2])
        rotor_right_backward= Cesar([ring_right[1], alphabet], rotor_centre_backward, ring_setting[2], 0)

        switched_letter_backward= plugboard(rotor_right_backward, switches)
        cipher+= switched_letter_backward

        if DEBUG:
            print(f'Keyboard input: {i}')
            print(f'Rotor positions: {ring_left[0][0]}{ring_centre[0][0]}{ring_right[0][0]}')            
            print(f'Plugboard: {i} -> {switched_letter_forward}')
            print(f'Rotor forward: {rotor_right_forward} -> {rotor_centre_forward} -> {rotor_left_forward}')
            print(f'Reflector: {reflector_in} -> {reflector_out}')
            print(f'Rotor backward: {rotor_right_backward} <- {rotor_centre_backward} <- {rotor_left_backward}')
            print(f'Plugboard: {switched_letter_backward} <- {rotor_right_backward}')
            print(f'Lampboard output: {switched_letter_backward}\n')
            
    return ' '.join([cipher[i: i + 5] for i in range(0, len(cipher), 5)])


def load(path):
    with open(path, 'r') as file:
        data= file.read()
    print(f'{path} loaded.')
    return data


def save(data, path):
    with open(path, 'w') as file:
        file.write(data)        
    print(f'{path} saved.')


def main():
    text= input('Type your text (letters only): ')
    #text= load('plaintext.txt')
    text= text.replace(' ', 'X')
    text= text.replace('.', 'X')
    text= text.replace(',', 'QQ')
    assert(text.isalpha())

    cipher= Enigma_process(text.upper())
    #save(cipher, 'Enigma_ciphertext.txt')
    print(f'\nCipher: {cipher}')
    

main()
