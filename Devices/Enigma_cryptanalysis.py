# -*- coding: utf-8 -*-
# /usr/bin/env python3
"""
Set of functions to analyze Egniam ciphertext, based on the logic of the TURING-WELCHMAN BOMBE.

I link my sources
https://www.turing.org.uk/scrapbook/ww2.html
https://en.wikipedia.org/wiki/Bombe
https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma

http://www.ellsbury.com/bombe1.htm
http://www.rutherfordjournal.org/article030108.html
https://www.101computing.net/turing-welchman-bombe/

"""

from collections import deque
from string import ascii_uppercase as AZ
from string import punctuation
from copy import copy
from itertools import permutations
from time import process_time
import re
from pprint import pprint

INNER_RING = {1: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              2: 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              3: 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
              4: 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
              5: 'VZBRGITYUPSDNHLXAWMJQOFECK',
              #6: 'JPGVOUMFYQBENHZRDKASXLICTW',
              #7: 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
              #8: 'FKQHTLXOCBJSPDZRAMEWNIUYGV'}

REFLECTOR = {'UKW_B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
             'UKW_C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}

TURN_NOTCH = {1: 'Q',                     # If rotor steps from Q to R, the next rotor is advanced
              2: 'E',	                  # If rotor steps from E to F, the next rotor is advanced
              3: 'V',	                  # If rotor steps from V to W, the next rotor is advanced
              4: 'J',	                  # If rotor steps from J to K, the next rotor is advanced
              5: 'Z',	                  # If rotor steps from Z to A, the next rotor is advanced 
              #6: ['Z', 'M'],              # If rotor steps from Z to A, or from M to N the next rotor is advanced
              #7: ['Z', 'M'],              # If rotor steps from Z to A, or from M to N the next rotor is advanced
              #8: ['Z', 'M']}              # If rotor steps from Z to A, or from M to N the next rotor is advanced

ROTOR_NAME = {1: 'I',
              2: 'II',
              3: 'III',
              4: 'IV',
              5: 'V',
              #6: 'VI',
              #7: 'VII',
              #8: 'VIII'}


              DEBUG = True
DEBUG_SOLUTION= {'Rotors': (1, 2, 3),
                 'Reflector': 'UKW_B',
                 'Start': ('A', 'B', 'C'),
                 'Ring settings': ('A', 'B', 'C')}


def Turing_Bombe(word, cipher):
    valid_cipher_positions = crib_analysis(word, cipher)                                                        # Returns cipher positions that yield a valid crib
    if not valid_cipher_positions:
        print('No cribs for this word')
        return None
    crib_index= int(input(f'Choose a crib to analyze. Possible index values {valid_cipher_positions}: '))       # Chose which crib to analyze  
    if crib_index not in valid_cipher_positions:
        print('The number you entered is not in the list')
        return None
    cipher_fragment= cipher[crib_index : crib_index + len(word)]                                                # Create the ciphertext fragment of the crib to analyze
    crib= dict(zip([i for i in range(len(word))], [ ''.join(i) for i in list(zip(word, cipher_fragment))]))     # Create a dict with crib positions as key and plain/cipher pairs as values      
    menu= []
    for letter in AZ:
        loops= prune(menu_analysis(crib, letter))                                                               # Create a list of loops for each letter in the alphabet 
        if len(loops) > 0:
            for loop in loops:
                menu.append([letter, loop])                                                                     # List letters for which at leats one loop exists                
    menu= dict(zip([i for i in range(len(menu))], menu))

    i= input('Scan rotor combinations [y/n]? ')
    assert(i.upper() == 'Y' or i.upper() == 'N')
    if i.upper() == 'Y':
        rotors, reflector= scan_rotors(word, cipher_fragment, menu, crib)
    else:
        rotors= (1, 2, 3)
        reflector= 'UKW_B'
    print(f'[+] Proceeding with rotors {rotors}')
    print(f'[+] Proceeding with reflector {reflector}')


    i= input('Scan start positions [y/n]? ')
    assert(i.upper() == 'Y' or i.upper() == 'N')
    if i.upper() == 'Y':
        start, ring_setting= scan_start(word, cipher_fragment, menu, crib, rotors, reflector)    
    else:
        start= ('Z', 'Z', 'Z')
        ring_setting= ('A', 'A', 'A')
    print(f'[+] Proceeding with start positions {start}')
    print(f'[+] Proceeding with ring settings {ring_setting}\n')

    pprint(menu)
    i= input('Choose the loops to complete a scan for plugboard combinations, separated by commas or spaces (A for all): ')
    if i.upper() == 'A':
        refined_menu= menu.values()
    else:
        i= re.sub('[, ]', ',', i)
        #i= i.split(',')
        refined_menu= [menu[int(j)] for j in i.split(',')]
    print('\nScannng loops for possible plugboard combinations:')
    plugboards= []
    for loop in refined_menu:
        switches= find_plugboard_combinations(rotors, loop[1], crib, reflector, start, ring_setting, True)
        if switches:
            plugboards= build_plugboard(switches, plugboards)
    
    print()
    for plugboard in plugboards:
        result= decode(rotors, reflector, start, ring_setting, plugboard, cipher_fragment, word)
        del result['Rotors']
        del result['Reflector']
        del result['Start']
        del result['Ring setting']
        print(result)


def build_plugboard(plugboards, switches):
    if len(plugboards) == 0:
        for s in switches:
            plugboards.append(s)
    else:
        for s in switches:
            for i, plugboard in enumerate(plugboards):
                if check_switch_pairs(s, plugboard):
                    plugboards[i]= s.union(plugboard)
    return plugboards


def scan_start(word, cipher_fragment, menu, crib, rotors, reflector):
    z= 'Y'
    start_combinations= None
    ring_setting= ('A', 'A', 'A')
    while z.upper() == 'Y':
        pprint(menu)
        n= int(input('Choose a loop to scan: '))
        setup= []
        if start_combinations:
            for s in start_combinations:
                for i in AZ:
                    start= (i, s[1], s[2]) 
                    print(f'\r[+] Testing start positions {start}', end= '\r', flush= True)
                    switches= find_plugboard_combinations(rotors, menu[n][1], crib, reflector, start, ring_setting, False)
                    if switches:
                        setup.append({'Start': start, 'Plugboard': switches})
        else:
            for i in AZ:
                for j in AZ:
                    start= ('Z', i, j)
                    print(f'\r[+] Testing start positions {start}', end= '\r', flush= True)
                    switches= find_plugboard_combinations(rotors, menu[n][1], crib, reflector, start, ring_setting, False)
                    if switches:
                        setup.append({'Start': start, 'Plugboard': switches})
        setup= dict(zip([i for i in range(len(setup))], setup))        
        print('\n')
        for i in setup:
            print(i, setup[i])
        z= input('Scan another loop [y/n]? ')
        start_combinations= [setup[i]['Start'] for i in setup]
    i= int(input('Choose the start positions: '))
    return setup[i]['Start'], ring_setting

  
  def scan_rotors(word, cipher_fragment, menu, crib):
    loop= list(menu.values())
    loop.sort(key= lambda x: len(x[1]))
    loop= loop[0]
    if DEBUG:
        begin= process_time()
    start= ('Z', 'Z', 'Z')
    ring_setting= ('A', 'A', 'A')
    setup= []
    for rotors in permutations(range(1, 6), 3):
        print(f'\r[+] Testing rotors {rotors}', end= '\r', flush= True)
        for reflector in REFLECTOR.keys():
            switches= find_plugboard_combinations(rotors, loop[1], crib, reflector, start, ring_setting, False)
            if not switches:
                setup.append(decode(rotors, reflector, start, ring_setting, switches, cipher_fragment, word))
            else:
                for switch in switches:
                    setup.append(decode(rotors, reflector, start, ring_setting, switch, cipher_fragment, word))
    setup.sort(key= lambda x: x['Matches'])
    setup= dict(zip([i for i in range(len(setup))], setup))
    print('\n')
    for i in setup:
        del setup[i]['Start']
        del setup[i]['Ring setting']
        del setup[i]['Text']
        if DEBUG:
            if setup[i]['Rotors'] == DEBUG_SOLUTION['Rotors']:
                print(i, setup[i], '<--')
            else:
                print(i, setup[i])
        else:
            print(i, setup[i])
    if DEBUG:
        print('Scan time: {0}'.format(process_time() - begin))
    i= int(input('Choose the rotors: '))
    return setup[i]['Rotors'], setup[i]['Reflector']


def decode(rotors, reflector, start, ring_setting, switch, cipher_fragment, word):
    left, centre, right= set_rotors(start, rotors)
    c= 0
    text= ''
    for index, letter in enumerate(cipher_fragment):
        left, centre, right= step_rotors(left, centre, right, rotors)
        enc_letter= rotors_encoding(letter, ring_setting, reflector, left, centre, right, switch if switch else '')
        text+= enc_letter
        if enc_letter == word[index]:
            c+= 1
    return {'Rotors': rotors, 'Reflector': reflector, 'Start': start, 'Ring setting': ring_setting, 'Matches': c, 'Plugboard': switch, 'Text': text}


def find_plugboard_combinations(rotors, loop, crib, reflector, start, ring_setting, plugboard_scan_display):
    valid_switches= []
    alphabets= [deque(AZ) for i in range(len(loop))]                                                   
    n= 0
    while n < len(AZ):
        letters_to_test= ''.join([i[0] for i in alphabets])
        if plugboard_scan_display:
            print(f'\r[+] Scanning loop {loop} for plugboard combinations {letters_to_test}', end= '\r')
        if check_letter_combinations(letters_to_test, list(i[1] for i in loop), crib):
            switches= compile_switches(letters_to_test, [j for i, j in loop], rotors, reflector, start, ring_setting, crib)
            if switches:
                switches= {''.join((min(i, j), max(i, j))) for i, j in switches}
                valid_switches.append(switches)    
        for i in range(len(alphabets)-1):
            if set(letters_to_test[i+1:]) == {'Z'}:
                alphabets[i].rotate(-1)
                if i == 0:
                    n+= 1
        alphabets[-1].rotate(-1)
    if plugboard_scan_display:
        print('\n')
    return valid_switches if valid_switches else None


def check_letter_combinations(letters_to_test, indexes, crib):
    previous_pairs= []
    for i, j in enumerate(indexes):
        pair= [''.join((crib[j][0], letters_to_test[i]))]
        if not check_switch_pairs(pair, previous_pairs):
            return False
        else:
            previous_pairs.extend(pair)
    return True


def compile_switches(letters, loop_indexes, rotors, reflector, start, ring_setting, crib):
    switches= []
    for i, j in enumerate(loop_indexes):
        left, centre, right= set_rotors(start, rotors)
        for step in range(j+1):
            left, centre, right= step_rotors(left, centre, right, rotors)       
        enc_letter= rotors_encoding(letters[i], ring_setting, reflector, left, centre, right, '')
        switch= [''.join((crib[j][0], letters[i])), ''.join((enc_letter, crib[j][1]))]
        if check_switch_pairs(switch, switches):
            switches.extend(switch)
        else:
            return None
    return switches


def check_switch_pairs(switch, other_switches):
    for i in switch:
        for j in other_switches:
            if i != j and i != j[::-1]:
                if i[0] in j or i[1] in j:
                    return False
    return True


def set_rotors(start, rotor):
    ring_left = [deque(AZ), deque(INNER_RING[rotor[0]])]
    offset = -1 * AZ.index(start[0])
    ring_left[0].rotate(offset)
    ring_left[1].rotate(offset)

    ring_centre = [deque(AZ), deque(INNER_RING[rotor[1]])]
    offset = -1 * AZ.index(start[1])
    ring_centre[0].rotate(offset)
    ring_centre[1].rotate(offset)

    ring_right = [deque(AZ), deque(INNER_RING[rotor[2]])]
    offset = -1 * AZ.index(start[2])
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


def Cesar(alphabets, letter, from_offset, to_offset):
    from_alphabet = copy(alphabets[0])
    from_alphabet.rotate(AZ.index(from_offset))

    to_alphabet = copy(alphabets[1])
    to_alphabet.rotate(AZ.index(to_offset))

    rot_tab = letter.maketrans(''.join(from_alphabet), ''.join(to_alphabet))
    return letter.translate(rot_tab)


def rotors_encoding(switched_letter_forward, ring_setting, reflector_type, ring_left, ring_centre, ring_right, switches):
    alphabet = deque(AZ)

    switched_letter_forward= plugboard(switched_letter_forward, switches)

    rotor_right_forward = Cesar([alphabet, ring_right[1]], switched_letter_forward, 'A', ring_setting[2])
    rotor_centre_forward = Cesar([ring_right[0], ring_centre[1]], rotor_right_forward, ring_setting[2], ring_setting[1])
    rotor_left_forward = Cesar([ring_centre[0], ring_left[1]], rotor_centre_forward, ring_setting[1], ring_setting[0])

    reflector_in = Cesar([ring_left[0], alphabet], rotor_left_forward, ring_setting[0], 'A')
    reflector_out = Cesar([deque(REFLECTOR[reflector_type]), ring_left[0]], reflector_in, 'A', ring_setting[0])

    rotor_left_backward = Cesar([ring_left[1], ring_centre[0]], reflector_out, ring_setting[0], ring_setting[1])
    rotor_centre_backward = Cesar([ring_centre[1], ring_right[0]], rotor_left_backward, ring_setting[1], ring_setting[2])
    rotor_right_backward = Cesar([ring_right[1], alphabet], rotor_centre_backward, ring_setting[2], 'A')

    rotor_right_backward= plugboard(rotor_right_backward, switches)

    return rotor_right_backward    


def plugboard(letter, switches):                                                               # If the input letter is in the list of switches, return the paired letter 
    for i, j in switches:
        if letter == i:
            return j
        elif letter == j:
            return i
    return letter


# function of menu analysis
def expand(crib, letter, reference):
    pairs= [''.join([crib[i][0], crib[i][1]]) for i in range(len(crib))]
    extensions= []
    for i in range(len(pairs)):
        if reference and i == reference:
            continue
        elif letter == pairs[i][0]:
            extensions.append((pairs[i], i))
        elif letter == pairs[i][1]:
            extensions.append((pairs[i][::-1], i))
    return extensions


# function of menu analysis
def branch(from_pairs, crib):
    to_pairs= []
    for i in range(len(from_pairs)):
        used_pairs= [z[1] for z in from_pairs[i]]
        if from_pairs[i][0][0][0] != from_pairs[i][len(from_pairs[i])-1][0][1]:                  
            extensions= expand(crib, from_pairs[i][len(from_pairs[i])-1][0][1], from_pairs[i][len(from_pairs[i])-1][1])
            for j in extensions:
                if j[1] not in used_pairs:
                    item= copy(from_pairs[i])
                    item.append(j)
                    to_pairs.append(item)
        else:
            to_pairs.append(from_pairs[i])
    return to_pairs


# function of menu analysis
def prune(menu):
    pruned_menu= copy(menu)
    global_indexes= []
    for i in range(len(menu)):
        if menu[i][0][0][0] != menu[i][len(menu[i])-1][0][1]:
            pruned_menu.remove(menu[i])
            continue
        if len(menu[i]) > 4:
            pruned_menu.remove(menu[i])
            continue
        loop_indexes= {j[1] for j in menu[i]}
        if loop_indexes in global_indexes:
            pruned_menu.remove(menu[i])
            continue
        else:
            global_indexes.append(loop_indexes)
        loop_indexes= []
        ref= ''
        for j in menu[i]:
            if j[0] == ref and len(menu[i]) > 2:
                pruned_menu.remove(menu[i])
                break
            if j[1] in loop_indexes:
                pruned_menu.remove(menu[i])
                break
            else:
                loop_indexes.append(j[1])
                ref= j[0][::-1]
    return pruned_menu


def menu_analysis(crib, start_letter):
    first_pairs= expand(crib, start_letter, None)                                           
    menu= []
    for i in range(len(first_pairs)):
        extensions= expand(crib, first_pairs[i][0][1], first_pairs[i][1])
        for j in extensions:
            item= copy([first_pairs[i]])
            item.append(j)
            menu.append(item)
    n= 0
    while len(menu) > n:
        n= len(menu)
        menu= branch(menu, crib)
    return menu


def crib_analysis(word, cipher):
    valid_cipher_positions = []
    for i in range(len(cipher) - len(word) + 1):                                            # Overlaps the known word with the cipher, shifting by one position at a time
        if DEBUG:
            print(f'\nChecking at index {i}:')
            print(word)
            print(f'{cipher[i:i+len(word)]}')
        if check_crib(word, cipher[i:i+len(word)]):                                         # If each letter of the word does not encrypt itself, it's a valid crib
            valid_cipher_positions.append(i)                                                # Append the index of the ciphertext into a list of valid indexes
            if DEBUG:
                print('Valid crib')
    return valid_cipher_positions


def check_crib(word, cipher_fragment):
    for i in range(len(word)):
        if word[i] == cipher_fragment[i]:                                                   # Check if any of the letters in the word encrypts itself in the cipher fragment
            return False
    return True


def load(path):                                                                             # Load function to eventually pull the ciphertext from a file
    with open(path, 'r') as file:
        text = file.read()
    print(f'Loaded:\n{text}\n')
    return text
    
    
def check_text(text):
    if DEBUG:
        for i, j in enumerate(text):
            if not j.isalpha():
                print(f'The char {j} at position {i} not a letter')
    assert(text.isalpha())                                                                  # Control if all the characters are letters, if not throws an assertion error


def prep_text(text):
    text = text.replace(' ', 'X')                                                           # In Enigma encryption spaces were normally replaced by X
    text = text.replace(',', 'QQ')                                                          # In Enigma encryption commas were normally replaced by QQ
    text = text.replace('\n', '')                                                           # Remove new line characters, needed when the text is loaded from a file                                                          # Remove new line characters, needed when the text is loaded from a file
    for p in punctuation:                                                                   # Remove all the remaining punctuation characters
        text = text.replace(p, '')
    check_text(text)                                                                        # Control if all the characters are letters, if not throws an assertion error
    return text


def main():
    try:
        cipher = load(r'Enigma_ciphertext.txt')
    except OSError:
        cipher= input('Paste an Enigma cipher: ')
    cipher = cipher.replace(' ', '')
    check_text(cipher)

    known_word = input('Type the suspected plaintext: ')
    known_word = prep_text(known_word)
    assert(len(known_word) <= len(cipher))                                                  # The ciphertext should not be shorter than the suspected word in plaintext

    Turing_Bombe(known_word.upper(), cipher.upper())


if __name__ == '__main__':
    main()
    
