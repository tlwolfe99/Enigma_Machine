#!/usr/bin/python3
# ===================================================================
# Enigma Machine Simulation - create configuration file
# ===================================================================

from EnigmaUtils import *

import copy
import re
import sys
import random
import user_interface as ui
from datetime import date

rotors = {'I':[], 'II':[], 'III':[],   'IV':[],
          'V':[], 'VI':[], 'VII':[], 'VIII':[] }


# ---------------------------------------------------------------
# ---- select alphabet
# ----
# ---- NOTES:
# ---- 1. AN ALPHABET MUST CONTAIN AN EVEN NUMBER OF CHARACTERS
# ---- 2. IT MUST NOT CONTAIN A COMMA
# ---------------------------------------------------------------

def select_alphabet():

    # ---- big alphabet (44 characters)
    alphabet0 = [ 'A','B','C','D','E','F','G','H','I','J','K','L',
                  'M','N','O','P','Q','R','S','T','U','V','W','X',
                  'Y','Z','1','2','3','4','5','6','7','8','9','0',
                  '.','=','+','-','/','*','(',')' ]

    # ---- enigma alphabet
    alphabet1 = [ 'A','B','C','D','E','F','G','H','I','J','K','L',
                  'M','N','O','P','Q','R','S','T','U','V','W','X',
                  'Y','Z' ]

    # ---- test alphabet
    alphabet2 = [ 'A','B','C','D','E','F' ]

    # ---- big alphabet (48 characters)
    alphabet3 = [ 'A','B','C','D','E','F','G','H','I','J','K','L',
                  'M','N','O','P','Q','R','S','T','U','V','W','X',
                  'Y','Z','1','2','3','4','5','6','7','8','9','0',
                  '.','=','+','-','/','*','(',')',' ','\\','"','\'' ]


    # ---- alphabet menu
    print('''select an alphabet for enigma configuration file

   option  description
   ------  ------------------------------------------------
     0     big    alphabet [ A-Z,0-9, ... ] (44 characters) 
     1     enigma alphabet [ A-Z ]
     2     test   alphabet [ A-F ]
     3     bigger alphabet [ A-Z,0-9, ... ] (48 characters)
     9     exit program''')

    # ---- make sure the alphabets have an even number of characters

    if len(alphabet0)%2 != 0 or \
       len(alphabet1)%2 != 0 or \
       len(alphabet2)%2 != 0 or \
       len(alphabet3)%2 != 0:
           print()
           print('Internal error: An alphabet contains an odd ')
           print('number of characters - end program')
           sys.exit()

    while True:

        print()
        s =ui.get_user_input('Select alphabet: ')

        if not s:
            sys.exit()

        tf,i = ui.is_int(s)

        if not tf:
            continue

        if i == 0:
            return alphabet0
        if i == 1:
            return alphabet1
        if i == 2:
            return alphabet2
        if i == 3:
            return alphabet3
        if i == 9:
            print()
            sys.exit()

        print()
        print(f'Unlnown alphabet selection (i)')
        continue

# ---------------------------------------------------------------
# ---- create plugboard connections (two unique characters)
# ---------------------------------------------------------------

def add_plugboard_connections(abc):

    plubs = []

    char_in_use = []

    # ---- display the current alphabet

    for i in range(len(abc)):
        if i % 12 == 0:
            print()
            print('Alphabet:',end='')
        print(f' {abc[i]}',end='')
    print()

    # ---- process user input         

    while True:

        print()
        s = ui.get_user_input('Enter plugboard connection (ab): ')

        if not s:
            break

        # ---- error check the user's input

        s = s.upper()

        if len(s) != 2 or s[0] == s[1]:
            print()
            print(f'Bad connection entered ({s})')
            continue

        c0 = s[0]
        c1 = s[1]

        if c0 not in abc:
            print()
            print(f'Character {c0} not in the alphabet')
            continue

        if c1 not in abc:
            print()
            print(f'Character {c1} not in the alphabet')
            continue

        if c0 in char_in_use:
            print()
            print(f'Character {c0} already in use')
            continue

        if c1 in char_in_use:
            print()
            print(f'Character {c1} already in use')
            continue

        # ---- save the user's input

        char_in_use.append(c0)
        char_in_use.append(c1)

        plugs.append(s)

    return plugs


# -------------------------------------------------------------------
# ---- main
# -------------------------------------------------------------------

# ---- select an alphabet

abc = select_alphabet()            # alphabet

abclen     = len(abc)              # abc list length
abcidx     = list(range(abclen))   # abc ordered list of indexes
configfile = 'enigma_config.csv'   # configuration file
plugs      = []                    # plugboard pairs list
reflst     = []                    # reflector list
today      = date.today()          # today's date

# ---- write enigma config file

line_count = 0                     # count, lines           written
plug_count = 0                     # count, plugs           written
refl_count = 0                     # count, reflector lists written
roto_count = 0                     # count, rotor lists     written

with open(configfile,"w") as f:

    # ---- add header lines to output file

    f.write(f'# Enigma Machine Simulation Configuration\n')
    line_count += 1

    f.write(f'date,{today}\n')
    line_count += 1

    # ---- add an unknown character substitution to the output file
    # ---- if an input character is not in the alphabet substitute
    # ---- a known character

    if len(abc) < 25:
        f.write(f'unk,{abc[-1]}\n')
    else:
        f.write('unk,X\n')
    line_count += 1

    # ---- output alphabet length

    f.write(f'len,{abclen}\n')
    line_count += 1

    # ---- add alphabet to output file

    f.write(f'# alphabet,list-idx,char\n')
    line_count += 1

    for i in range(abclen):
        f.write(f'abc,{i},{abc[i]}\n')
        line_count += 1

    # ---- create rotor lists and add them to the output file

    for r in rotors: 

        ranlst = create_randomized_rotor_list(abcidx)

        rotors[r] = ranlst     # save it for later counting

        f.write(f'# rotor-name,in-list-idx,out-list-idx,in-char,out-char\n')
        line_count += 1

        for i in range(len(ranlst)):
            j = ranlst[i]
            f.write(f'{r},{i},{j},{abc[i]},{abc[j]}\n')
            line_count += 1

        roto_count += 1

    # ---- create reflector list and add it to the output file

    reflst = create_randomized_reflector_list(abcidx)

    f.write(f'# reflector,in-list-idx,out-list-idx,in-char,out-char\n')
    line_count += 1

    for i in range(abclen):
        j = reflst[i]
        f.write(f'ref,{i},{j},{abc[i]},{abc[j]}\n')
        line_count += 1

    # ---- verify reflector pairs

    for i in range(abclen):
        j = reflst[i]
        if reflst[j] != i: 
            print(f'Error in reflector list i={i} j={j}')
            print(f'reflst[{i}] = {reflst[i]}')
            print(f'reflst[{j}] = {reflst[j]}')
            sys.exit()

    refl_count += 1

    # ---- add plugboard connections to the output file

    plubs = add_plugboard_connections(abc)

    l = len(plugs)

    print()
    if l == 0:
        print('No plugboard connections')
    else:
        print(f'{l} plugboard connections')
        f.write(f'# plugboard,char-pair\n')
        line_count += 1
        for i in range(l):
            f.write(f'plug,{plugs[i]}\n')
            line_count += 1

# ---- display stats

print()
print(f'date         : {today}')  
print(f'file     name: {configfile}')
print(f'abc       len: {abclen}')
print(f'alphabet  len: {len(abc)}')
print(f'rotor   count: {len(rotors)}')
for r in rotors.keys():
    print(f'  {r:5}   len: {len(rotors[r])}')
print(f'reflector len: {len(reflst)}')
print(f'plugs        : {len(plugs)}')
print(f'lines written: {line_count}')
print()
