#/usr/bin/env python3

# DRAFT WIP

"""
ENIGMA DEVICE MODEL M3, VARIATION IN USE BY GERMAN NAVY (KRIEGSMARINE)
Launched in 1940, part of a family of rotor based cipher machines.


A PLUGBOARD
The keyboard inputs were processed first through a plugboard.
The plugboard cables were set to switch letters, serving as first substitution cipher step between keyboard and rotors.


THREE ROTORS
The signal from the plugboard proceeded then through 3 rotors in separate slots, from right to left. A total of 5 rotors were available to chose from.
The version used in the avy had additional 3 rotors, for a total of 8. The rotors were coded with roman letters, from I to VIII.

Every time a key was pressed, the rotor on the right turned by 1 letter before encrypting the signal (2 letters for rotors 6, 7 and 8). 
When the right wheel rotation reached a turnover point (called "notch point"), the middle rotor advanced by one step, and so on. 
The letters in each rotor were also wired differently to encode shuffled alphabet letters.
Such letters can be additional shifted by an arbitrary number, for each rotor ("ring settings").

This meant that the encryption settings constantly changed for each letter of a message, 
and that a single plaintext letter would be encrypted differently depending on its position in the message.


A REFLECTOR
After the rotors, the encryption flowed through a "reflector" (or "reversing drum"), an additional electrical rotor in fixed position.
The Enigma M series were equipped with reflector models UKW-B or UKW-C, each applying a different substitution.


SIGNAL BACKWARDS
After the reflector, the signal returned backwards, through the 3 rotors in reverse order, then through the plugboard, and recorded into a lampboard,
which displayed the encryption.


THE SETTINGS
The initial daily setup of the devices was written in a military "code book". An Enigma code book would have one page per month. 
The page would include all the settings for each day of the month with the first day of the month at the bottom of the page so that once used, 
a setting could be torn off the page. Setting example:
30              Day of the month
IV II III       Rotor numbers and positions (left - middle - right)
UDZ             Ring setting, applying an additional shift to the letters in the rotor
DW AO QT        Plugboard switches (in this examples D to W, A to O and Q to T are active)
AFJ             Initial position of the rotors
"""

import random
from collections import deque
from string import ascii_uppercase as AZ
from copy import copy

# Internal wirings and mechanics of the rotors
# https://en.wikipedia.org/wiki/Enigma_rotor_details

ROTOR_WIRING= {1:'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
               2:'AJDKSIRUXBLHWTMCQGZNPYFVOE',
               3:'BDFHJLCPRTXVZNYEIWGAKMUSQO',
               4:'ESOVPZJAYQUIRHXLNFTGKDCMWB',
               5:'VZBRGITYUPSDNHLXAWMJQOFECK',
               6:'JPGVOUMFYQBENHZRDKASXLICTW',
               7:'NZJHGRCXMYSWBOUFAIVLPEKQDT',
               8:'FKQHTLXOCBJSPDZRAMEWNIUYGV'}


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

STEP= {1:1,
       2:1,
       3:1,
       4:1,
       5:1,
       6:2,
       7:2,
       8:2}
            
SIMPLIFY= True

def setup_Enigma():
    if SIMPLIFY:
        rotors= (1, 2, 3)
        switches= []
        start= ('A', 'A', 'T')
        ring_set= ('A', 'A', 'A')
        reflector= 'UKW_B'
    else:
        rotors= tuple(random.sample([i for i in range(1, 9)], k= 3))
        ring_set= tuple(random.choices(AZ, k= 3))
        start= tuple(random.choices(AZ, k= 3))
        reflector= ''.join(random.choices(list(REFLECTOR.keys()), k= 1))
        
        switches= []
        first_letters= random.sample(AZ, k= 6)
        second_letters= copy(AZ)
        for i in first_letters:
            j= random.sample([n for n in second_letters if n != i], k= 1)[0]
            switches.append((i, j))
            second_letters= second_letters.replace(f'{j}', '')
    return rotors, ring_set, start, reflector, tuple(switches)


def print_setup(rotors, shift, start, reflector, switches):
    print(f'Rotors: {rotors}')
    print(f'Ring settings: {shift}')
    print(f'Plugboard switches: {switches}')
    print(f'Start positions: {start}')
    print(f'Reflector type: {reflector}')


def plugboard_switches(letter, switches):
    for i, j in switches:
        if letter == i:
            return j
    return letter


def start_rotors(position):
    alphabet= [i for i in AZ]
    
    left= deque(copy(alphabet))
    left.rotate(-left.index(position[0]))
    
    middle= deque(copy(alphabet))
    middle.rotate(-middle.index(position[1]))
    
    right= deque(copy(alphabet))
    right.rotate(-right.index(position[2]))
    
    return left, middle, right


def step_rotors(left, middle, right, rotors):
    for i in range(STEP[rotors[2]]):
        if right[0] in TURN_NOTCH[rotors[2]]:
            for j in range(STEP[rotors[1]]):
                if middle[0] in TURN_NOTCH[rotors[1]]:
                    for k in range(STEP[rotors[0]]):
                        left.rotate(-1)
                middle.rotate(-1)
        right.rotate(-1)
    return left, middle, right


def rotor_substitution(letter, left, middle, right, settings, rotors):
    letter= Cesar(right, letter, settings[2])
    #letter= Cesar()                                        # it misses inner wirings
    letter= Cesar(middle, letter, settings[1])
    return Cesar(left, letter, settings[0])


def reflector_substitution(letter, reflect_type):
    no_additional_shift= 'A'
    return Cesar(REFLECTOR[reflect_type], letter, no_additional_shift)


def Cesar(new_alphabet, letter, additional_shift):
    new_alphabet= copy(new_alphabet)
    if additional_shift != 'A':
        new_alphabet.rotate(ord(additional_shift) - ord('A'))
    rot_tab= letter.maketrans(AZ, ''.join(new_alphabet))                   
    cipher= letter.translate(rot_tab)
    return cipher


def reverse_switches(switches):
    return ((j, i) for i, j in switches)


def encrypt(text, rotors, settings, start_positions, reflect_type, switches):
    left, middle, right= start_rotors(start_positions)
    cipher= ''    
    for i in text:
        letter= plugboard_switches(i, switches)
        print(''.join(right))
        left, middle, right= step_rotors(left, middle, right, rotors)
        letter= rotor_substitution(letter, left, middle, right, settings, rotors)
        letter= reflector_substitution(letter, reflect_type)
        letter= rotor_substitution(letter, right, middle, left, settings[::-1], rotors[::-1])
        letter= plugboard_switches(letter, reverse_switches(switches))
        cipher+= letter
    
    return ' '.join([cipher[i: i + 5] for i in range(0, len(cipher), 5)])
        

def main():
    text= 'attackatdawn' #input('Type your text (letters only): ')
    text= text.replace(' ', '').upper()
    assert(text.isalpha())
    
    rotors, settings, start, reflect_type, switches= setup_Enigma()
    print_setup(rotors, settings, start, reflect_type, switches)

    cipher= encrypt(text, rotors, settings, start, reflect_type, switches)
    print(f'\nCipher: {cipher}')

main()

