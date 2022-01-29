#!/usr/bin/python3
# ===================================================================
# Enigma Machine Simulation - test enigma rotor
# ===================================================================

from EnigmaRotor import EnigmaRotor
from EnigmaConfig import EnigmaConfig
import user_interface as ui
import os
import sys

# -------------------------------------------------------------------
# ---- main - test enigma rotor
# -------------------------------------------------------------------

# ---- get configuration file

configfile = 'enigma_config.csv'

if len(sys.argv) > 1:
    configfile = sys.argv[1]

if not os.path.exists(configfile):
    print()
    print(f'Can not find enigma configuration file ({configfile})') 
    print()
    sys.exit()

ec = EnigmaConfig('enigma_config.csv')

keys = list(ec.rotors.keys())

rotor = EnigmaRotor(ec,'I',0)

while True:

    print()
    rotor.display('------Initial configuration ---------',True)

    # ---- get rotor name

    while True:
        print()
        s1 = ui.get_user_input('Enter new rotor name: ')
        if not s1:
            sys.exit()
        if s1 not in keys:
            print()
            print(f'illegal rotor name ({s1})')
            print(f'legal names are {keys}')
            continue     
        break
    
    # ---- get rotor start

    while True:
        print()
        s2 = ui.get_user_input('Enter new rotor start: ')
        if not s2:
            sys.exit()
        tf,x = ui.is_integer(s2)
        if not tf:
            sys.exit()
        if x < 0 or x >= ec.abclen:
            print()
            print(f'illegal rotor start ({s2})')
            print(f'start must be less than {ec.abclen}')
            continue
        break

    # ---- adjust rotor

    rotor.reset(s1,x)

    rotor.display('-----new rotor configurtion -----',True)

