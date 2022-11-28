#/usr/bin/env python3
"""
ENIGMA MODEL M4
Introduced in 1942 for certain divisions of the Kriegsmarine, in particular for the U-Boats.
Its traffic was known as "SHARK" by the allies codebreakers.

In the model M4, an extra wheel was added to the M4, to the left of the three regular wheels.
This extra wheel adds an additional stage to the encryption algorithm. 
The extra wheel does not move when entering a message and is not interchangeable with the other wheels.
When the extra wheel is placed at position A, the machine is backwards compatible with the 3-wheel Enigma I and the Enigma M3.

Note that the extra wheel is not driven by the wheel to its right, so it never moves when typing a message.

"""

import secrets
from collections import deque
from string import ascii_uppercase as AZ
from string import punctuation
from copy import copy


TEXT = 'Type your text here...'


INNER_RING = {1:'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              2:'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              3:'BDFHJLCPRTXVZNYEIWGAKMUSQO',
              4:'ESOVPZJAYQUIRHXLNFTGKDCMWB',
              5:'VZBRGITYUPSDNHLXAWMJQOFECK',
              6:'JPGVOUMFYQBENHZRDKASXLICTW',
              7:'NZJHGRCXMYSWBOUFAIVLPEKQDT',
              8:'FKQHTLXOCBJSPDZRAMEWNIUYGV'}

REFLECTOR = {'B_Thin':'ENKQAUYWJICOPBLMDXZVFTHRGS',		
             'C_Thin':'RDOBJNTKVEHMLFCWZAXGYIPSUQ'}

ADDITIONAL_WHEEL = {'Beta':'LEYJVCNIXWPBQMDRTAKZGFUHOS',
                    'Gamma':'FSOKANUERHMBTIYCWLQPZXVGJD'}

TURN_NOTCH = {1:'Q',           # If rotor steps from Q to R, the next rotor is advanced
              2:'E',	          # If rotor steps from E to F, the next rotor is advanced
              3:'V',	          # If rotor steps from V to W, the next rotor is advanced
              4:'J',	          # If rotor steps from J to K, the next rotor is advanced
              5:'Z',	          # If rotor steps from Z to A, the next rotor is advanced
              6:['Z', 'M'],    # If rotor steps from Z to A, or from M to N the next rotor is advanced
              7:['Z', 'M'],    # If rotor steps from Z to A, or from M to N the next rotor is advanced
              8:['Z', 'M']}    # If rotor steps from Z to A, or from M to N the next rotor is advanced

ROTOR_NAME = {1:'I',
              2:'II', 
              3:'III',
              4:'IV',
              5:'V',
              6:'VI',
              7:'VII',
              8:'VIII'}

MANUAL_SETUP = False
DEBUG = False


def setup():
    if MANUAL_SETUP:
        rotor = (1, 2, 3)
        switches = []                                                            
        start = ('B', 'B', 'D', 'U')
        ring_setting = ('A', 'A', 'A', 'A')
        reflector = 'B_Thin'
        thin_wheel = 'Beta'
        assert(check_manual_setup(rotor, switches, start, ring_setting, reflector, thin_wheel))
    else:
        rotors = list(range(1, 9))
        rotor = tuple(rotors.pop(rotors.index(secrets.choice(rotors))) for i in range(3))               # Rotors: random sample of three unique values from 1 to 8
        ring_setting = tuple(secrets.choice(AZ) for i in range(4))                                      # Ring settings: Tuple of 3 random letters from the alphabet AZ
        start = tuple(secrets.choice(AZ) for i in range(4))                                             # Start positions: Tuple of 3 random letters from the alphabet AZ        
        reflector = secrets.choice(list(REFLECTOR.keys()))                                              # Reflector type: Chose randomly between the two keys assigned to REFLECTOR dictionary
        thin_wheel = secrets.choice(list(ADDITIONAL_WHEEL.keys()))
        
        switches = []
        alphabet = list(AZ)
        first_letters = set(alphabet.pop(alphabet.index(secrets.choice(alphabet))) for i in range(10))  # Generate 10 random unique letters
        second_letters = list(set(copy(AZ)).difference(first_letters))                                  # Create a string the all the remaining letters of the alphabet AZ
        for i in first_letters:                                                                         # For each letter in the list of 10 randomly generated:
            switches.append((i, second_letters.pop(second_letters.index(secrets.choice(second_letters)))))                                                                     
          
    print(f'Rotors: {thin_wheel}, {ROTOR_NAME[rotor[0]]}, {ROTOR_NAME[rotor[1]]}, {ROTOR_NAME[rotor[2]]}')
    print(f'Ring settings: {ring_setting[0]}, {ring_setting[1]}, {ring_setting[2]}, {ring_setting[3]}')
    print(f'Start positions: {start[0]}, {start[1]}, {start[2]}, {start[3]}')
    print(f'Reflector type: {reflector}')
    print(f'Plugboard switches: {switches}\n')

    return rotor, ring_setting, start, reflector, switches, thin_wheel

  
def check_manual_setup(rotor, switches, start, ring_setting, reflector, thin_wheel):
    if len(set(rotor)) != 3:
        return False
    for i in rotor:
        if type(i) is not int:
            return False
    if len(start) != 4:
        return False
    for i in start:
        if type(i) is not str:
            return False
    if len(ring_setting) != 4:
        return False
    for i in ring_setting:
        if type(i) is not str:
            return False
    if reflector not in REFLECTOR:
        return False
    if thin_wheel not in ADDITIONAL_WHEEL:
        return False
    for i in switches:
        other_switches= copy(switches)
        other_switches.remove(i)
        for j in other_switches:
            if i != j and i != j[::-1]:
                if i[0] in j or i[1] in j:
                    return False
    return True
  

def set_rotors(start, rotor, wheel_type):
    thin_wheel = [deque(AZ), deque(ADDITIONAL_WHEEL[wheel_type])]
    offset = -1 * AZ.index(start[0])
    thin_wheel[0].rotate(offset)
    thin_wheel[1].rotate(offset)
    
    ring_left = [deque(AZ), deque(INNER_RING[rotor[0]])]
    offset = -1 * AZ.index(start[1])
    ring_left[0].rotate(offset)
    ring_left[1].rotate(offset)
    
    ring_centre = [deque(AZ), deque(INNER_RING[rotor[1]])]
    offset = -1 * AZ.index(start[2])
    ring_centre[0].rotate(offset)
    ring_centre[1].rotate(offset)
    
    ring_right = [deque(AZ), deque(INNER_RING[rotor[2]])]
    offset = -1 * AZ.index(start[3])
    ring_right[0].rotate(offset)
    ring_right[1].rotate(offset)
    
    return ring_left, ring_centre, ring_right, thin_wheel
    

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
    from_alphabet = copy(alphabets[0])
    from_alphabet.rotate(AZ.index(from_offset))

    to_alphabet = copy(alphabets[1])
    to_alphabet.rotate(AZ.index(to_offset))

    rot_tab = letter.maketrans(''.join(from_alphabet), ''.join(to_alphabet))                   
    return letter.translate(rot_tab)

   
def Enigma_process(text, rotors, ring_setting, start_positions, reflector_type, switches, thin_wheel_type):
    ring_left, ring_centre, ring_right, thin_wheel = set_rotors(start_positions, rotors, thin_wheel_type)
    alphabet = deque(AZ)
    
    enc_text = ''    
    for i in text:    
        ring_left, ring_centre, ring_right = step_rotors(ring_left, ring_centre, ring_right, rotors)
        
        switched_letter_forward = plugboard(i, switches)
        
        rotor_right_forward = Cesar([alphabet, ring_right[1]], switched_letter_forward, 'A', ring_setting[3])
        rotor_centre_forward = Cesar([ring_right[0], ring_centre[1]], rotor_right_forward, ring_setting[3], ring_setting[2])
        rotor_left_forward = Cesar([ring_centre[0], ring_left[1]], rotor_centre_forward, ring_setting[2], ring_setting[1])
        
        additional_wheel_forward = Cesar([ring_left[0], thin_wheel[1]], rotor_left_forward, ring_setting[1], ring_setting[0])
        
        reflector_in = Cesar([thin_wheel[0], alphabet], additional_wheel_forward, ring_setting[0], 'A')
        reflector_out = Cesar([deque(REFLECTOR[reflector_type]), thin_wheel[0]], reflector_in, 'A', ring_setting[0])
        
        additional_wheel_backward = Cesar([thin_wheel[1], ring_left[0]], reflector_out, ring_setting[0], ring_setting[1])
        
        rotor_left_backward = Cesar([ring_left[1], ring_centre[0]], additional_wheel_backward, ring_setting[1], ring_setting[2])
        rotor_centre_backward = Cesar([ring_centre[1], ring_right[0]], rotor_left_backward, ring_setting[2], ring_setting[3])
        rotor_right_backward = Cesar([ring_right[1], alphabet], rotor_centre_backward, ring_setting[3], 'A')
        
        switched_letter_backward = plugboard(rotor_right_backward, switches)
        enc_text += switched_letter_backward

        if DEBUG:
            print(f'Keyboard input: {i}')
            print(f'Rotor positions: {ring_left[0][0]}{ring_centre[0][0]}{ring_right[0][0]}')            
            print(f'Plugboard: {i} -> {switched_letter_forward}')
            print(f'Rotor forward: {rotor_right_forward} -> {rotor_centre_forward} -> {rotor_left_forward} -> {additional_wheel_forward}')
            print(f'Reflector: {reflector_in} -> {reflector_out}')
            print(f'Rotor backward: {rotor_right_backward} <- {rotor_centre_backward} <- {rotor_left_backward} <- {additional_wheel_backward}')
            print(f'Plugboard: {switched_letter_backward} <- {rotor_right_backward}')
            print(f'Lampboard output: {switched_letter_backward}\n')
            
    return ' '.join([enc_text[i:i + 5] for i in range(0, len(enc_text), 5)])
        

def prep_text(text):                                                                                                                # Replace common puctuation with letters
    text = text.replace(' ', 'X')
    text = text.replace(',', 'QQ')
    for p in punctuation:
        text = text.replace(p, '')
    assert(text.isalpha())
    return text


if __name__ == '__main__':
    text = prep_text(TEXT)
    rotors, ring_setting, start_positions, reflector_type, switches, thin_wheel_type = setup()
    enc_text = Enigma_process(text.upper(), rotors, ring_setting, start_positions, reflector_type, switches, thin_wheel_type)
    print(f'\nCiphertext: {enc_text}')
