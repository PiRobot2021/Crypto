#/usr/bin/env python3
"""
ENIGMA MODEL M3 (incl. KRIEGSMARINE wheels)
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
from string import punctuation
from copy import copy

#            -> ABCDEFGHIJKLMNOPQRSTUVWXYZ <-
INNER_RING= {1:'EKMFLGDQVZNTOWYHXUSPAIBRCJ',        # This represents the internal wiring of the alphabet in each rotors
             2:'AJDKSIRUXBLHWTMCQGZNPYFVOE',
             3:'BDFHJLCPRTXVZNYEIWGAKMUSQO',
             4:'ESOVPZJAYQUIRHXLNFTGKDCMWB',
             5:'VZBRGITYUPSDNHLXAWMJQOFECK',
             6:'JPGVOUMFYQBENHZRDKASXLICTW',
             7:'NZJHGRCXMYSWBOUFAIVLPEKQDT',
             8:'FKQHTLXOCBJSPDZRAMEWNIUYGV'}


#                 -> ABCDEFGHIJKLMNOPQRSTUVWXYZ <-
REFLECTOR= {'UKW_B':'YRUHQSLDPXNGOKMIEBFZCWVJAT',	  # The letters in the reflector are mirrored (e.g. A -> Y, so Y -> A):
            'UKW_C':'FVPJIAOYEDRZXWGCTKUQSBNMHL'}

TURN_NOTCH= {1:'Q',                                 # If rotor steps from Q to R, the next rotor is advanced
             2:'E',	                                # If rotor steps from E to F, the next rotor is advanced
             3:'V',	                                # If rotor steps from V to W, the next rotor is advanced
             4:'J',	                                # If rotor steps from J to K, the next rotor is advanced
             5:'Z',	                                # If rotor steps from Z to A, the next rotor is advanced
             6:['Z', 'M'],                          # If rotor steps from Z to A, or from M to N the next rotor is advanced
             7:['Z', 'M'],                          # If rotor steps from Z to A, or from M to N the next rotor is advanced
             8:['Z', 'M']}                          # If rotor steps from Z to A, or from M to N the next rotor is advanced

ROTOR_NAME= {1:'I',                                 # It beautifies the printed rotor numbers on screen to roman letters
             2:'II', 
             3:'III',
             4:'IV',
             5:'V',
             6:'VI',
             7:'VII',
             8:'VIII'}

MANUAL_SETUP= False                                 # Set to True to enter custom parameters in the setup() function
DEBUG= False

def setup():
    if MANUAL_SETUP:
        rotor= (1, 2, 3)                                                          # Chose the rotors to use, from 1 to 8. A rotor can be set only once.
        switches= [('A', 'B')]                                                    # List up to 13 pairs of letters to simulate the plugboard, represented as tuples. A letter can be used only once.                                     
        start= ('A', 'D', 'U')                                                    # Three letter values, setting the start positions of the rotors.
        ring_setting= (0, 0, 0)                                                   # Internal shift of the ring against the start positions. Each value varies from 0 to 25 (equivalent of A to Z).
        reflector= 'UKW_B'                                                        # The reflector type: Can be either UKW_B or UKW_C.
    else:                                                                         # Switch to automatic mode, setup is randomly generated      
        rotor= tuple(random.sample(range(1, 9), k= 3))                            # Rotors: random sample of three unique values from 1 to 8
        ring_setting= tuple(random.choices(range(26), k= 3))                      # Ring settings: Tuple of 3 random values from 0 to 25, equivalent to A to Z
        start= tuple(random.choices(AZ, k= 3))                                    # Start positions: Tuple of 3 random letters from the alphabet AZ        
        reflector= ''.join(random.choices(list(REFLECTOR.keys()), k= 1))          # Reflector type: Chose randomly between the two keys assigned to REFLECTOR dictionary
        
        switches= []
        first_letters= random.sample(AZ, k= 10)                                   # Generate 10 random unique letters
        second_letters= ''.join(set(copy(AZ)).difference(set(first_letters)))     # Create a string the all the remaining letters of the alphabet AZ
        for i in first_letters:                                                   # For each letter in the list of 10 randomly generated:
            j= random.sample(second_letters, k= 1)[0]                             # Chose a random letter from the string of remaining letters
            switches.append((i, j))                                               # Append it to the first letter to form a tuple
            second_letters= second_letters.replace(f'{j}', '')                    # Remove the appended letter from the remaining letters 
    assert(check_setup(rotor, switches, start, ring_setting, reflector)) 
    print(f'Rotors: {ROTOR_NAME[rotor[0]]}, {ROTOR_NAME[rotor[1]]}, {ROTOR_NAME[rotor[2]]}')
    print(f'Ring settings: {AZ[ring_setting[0]]}, {AZ[ring_setting[1]]}, {AZ[ring_setting[2]]}')
    print(f'Start positions: {start[0]}, {start[1]}, {start[2]}')
    print(f'Reflector type: {reflector}')
    print(f'Plugboard switches: {switches}\n')
    return rotor, ring_setting, start, reflector, switches

  
def check_setup(rotor, switches, start, ring_setting, reflector):
    if len(set(rotor)) != 3:
        return False
    for i in rotor:
        if type(i) is not int:
            return False
    if len(start) != 3:
        return False
    for i in start:
        if type(i) is not str:
            return False
    if len(ring_setting) != 3:
        return False
    for i in ring_setting:
        if type(i) is not int:
            return False
    if reflector not in REFLECTOR.keys():
        return False
    for i in switches:
        other_switches= copy(switches)
        other_switches.remove(i)
        for j in other_switches:
            if i != j and i != j[::-1]:
                if i[0] in j or i[1] in j:
                    return False
    return True
  

def set_rotors(start, rotor):                                                     # Simulate the rotors as deques. Setup the starting positions by rotating the deques
    ring_left= [deque(AZ), deque(INNER_RING[rotor[0]])]                           # Each rotor is represented a as list containing the two side of the inner ring, as deques
    offset= -1 * AZ.index(start[0])                                               # Create an offset from the starting position of the setup function
    ring_left[0].rotate(offset)                                                   # Rotate one side of the rotor
    ring_left[1].rotate(offset)                                                   # Align the other side of the rotor to the same rotation
    
    ring_centre= [deque(AZ), deque(INNER_RING[rotor[1]])]
    offset= -1 * AZ.index(start[1])
    ring_centre[0].rotate(offset)
    ring_centre[1].rotate(offset)
    
    ring_right= [deque(AZ), deque(INNER_RING[rotor[2]])]
    offset= -1 * AZ.index(start[2])
    ring_right[0].rotate(offset)
    ring_right[1].rotate(offset)
    
    return ring_left, ring_centre, ring_right
    

def step_rotors(ring_left, ring_centre, ring_right, rotor):                       # Step the rotors according to the Enigma specification (single, double, triple steps).
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


def plugboard(letter, switches):                                                               # If the input letter is in the list of switches, return the paired letter 
    for i, j in switches:
        if letter == i:
            return j
        elif letter == j:
            return i
    return letter


def Cesar(alphabets, letter, from_offset, to_offset):                                          # This funciton returns the input letter shifted according to rotors and ring settings
    from_alphabet= copy(alphabets[0])                                                          # Create a copy of the alphabet position in the source rotor
    from_alphabet.rotate(from_offset)                                                          # I apply the ring setting as offsets from the current rotor position. Rotate the source alphabet to the offset from ring setting.

    to_alphabet= copy(alphabets[1])
    to_alphabet.rotate(to_offset)

    rot_tab= letter.maketrans(''.join(from_alphabet), ''.join(to_alphabet))                   # Translate the letter and return it
    return letter.translate(rot_tab)

   
def Enigma_process(text, rotors, ring_setting, start_positions, reflector_type, switches):
    ring_left, ring_centre, ring_right= set_rotors(start_positions, rotors)                                                         # Set the rotors and the satrt positions
    alphabet= deque(AZ)                                                                                                             # Create a deque of the alphabet, for the fixed parts of the Enigma
    
    cipher= ''    
    for i in text:                                                                                                                  # For each letter in the plaintext:
        ring_left, ring_centre, ring_right= step_rotors(ring_left, ring_centre, ring_right, rotors)                                 # Step the rotors before the encryption
        
        switched_letter_forward= plugboard(i, switches)                                                                             # Process the plaintext letter thorugh the plugboard
        
        rotor_right_forward= Cesar([alphabet, ring_right[1]], switched_letter_forward, 0, ring_setting[2])                          # Process the encrypted letter forward through the rotors
        rotor_centre_forward= Cesar([ring_right[0], ring_centre[1]], rotor_right_forward, ring_setting[2], ring_setting[1])
        rotor_left_forward= Cesar([ring_centre[0], ring_left[1]], rotor_centre_forward, ring_setting[1], ring_setting[0])

        reflector_in= Cesar([ring_left[0], alphabet], rotor_left_forward, ring_setting[0], 0)                                       # Process the encrypted letter through the reflector
        reflector_out= Cesar([deque(REFLECTOR[reflector_type]), ring_left[0]], reflector_in, 0, ring_setting[0])
        
        rotor_left_backward= Cesar([ring_left[1], ring_centre[0]], reflector_out, ring_setting[0], ring_setting[1])                 # Process the encrypted letter backward through the rotors
        rotor_centre_backward= Cesar([ring_centre[1], ring_right[0]], rotor_left_backward, ring_setting[1], ring_setting[2])
        rotor_right_backward= Cesar([ring_right[1], alphabet], rotor_centre_backward, ring_setting[2], 0)

        switched_letter_backward= plugboard(rotor_right_backward, switches)                                                         # Process the encrypted letter through the plugboard
        cipher+= switched_letter_backward                                                                                           # Attache the encrypted letter to the ciphertext

        if DEBUG:
            print(f'Keyboard input: {i}')
            print(f'Rotor positions: {ring_left[0][0]}{ring_centre[0][0]}{ring_right[0][0]}')            
            print(f'Plugboard: {i} -> {switched_letter_forward}')
            print(f'Rotor forward: {rotor_right_forward} -> {rotor_centre_forward} -> {rotor_left_forward}')
            print(f'Reflector: {reflector_in} -> {reflector_out}')
            print(f'Rotor backward: {rotor_right_backward} <- {rotor_centre_backward} <- {rotor_left_backward}')
            print(f'Plugboard: {switched_letter_backward} <- {rotor_right_backward}')
            print(f'Lampboard output: {switched_letter_backward}\n')
            
    return ' '.join([cipher[i: i + 5] for i in range(0, len(cipher), 5)])                                                          # Return cipher in groups of 5 letters


def load(path):                                                                 # Load plaintext from a file
    with open(path, 'r') as file:
        data= file.read()
    print(f'{path} loaded.')
    return data


def save(data, path):                                                           # Save ciphertext into a file
    with open(path, 'w') as file:
        file.write(data)        
    print(f'{path} saved.')


def check_text(text):                                                           # Control if the plaintext only contains letters, if not, throw an assertion error
    if DEBUG:
        for i, j in enumerate(text):
            if not j.isalpha():
                print(f'The char {j} at position {i} not a letter')
    assert(text.isalpha())


def prep_text(text):                                                            # Replace common puctuation with letters
    text= text.replace(' ', 'X')
    text= text.replace(',', 'QQ')
    text= text.replace('\n', '')
    text= text.replace('\r', '')
    for p in punctuation:
        text= text.replace(p, '')
    check_text(text)
    return text
  
  
def main():
    text= input('Type your text (no digits): ')
    #text= load(r'plaintext.txt')
    text= prep_text(text)
    
    rotors, ring_setting, start_positions, reflector_type, switches= setup()                                                        # Load the setup of the device
    cipher= Enigma_process(text.upper(), rotors, ring_setting, start_positions, reflector_type, switches)
    #save(cipher, r'Enigma_ciphertext.txt')
    print(f'\nCipher: {cipher}')
    

if __name__ == '__main__':
    main()
