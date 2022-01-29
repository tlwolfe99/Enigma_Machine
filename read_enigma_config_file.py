#!/usr/bin/python3
# ===================================================================
# Enigma Machine Simulation - read configuration file
# ===================================================================

import re
import os
import sys
import user_interface as ui

abc        = []
abclen     = 0
abcunk     = None
configfile = 'enigma_config.csv'
date       = None
line_count = 0
plugs      = []
reflst     = []
rotors     = {  'I':[], 'II':[], 'III':[],   'IV':[],
                'V':[], 'VI':[], 'VII':[], 'VIII':[] }

# -------------------------------------------------------------------
# ---- read enigma machine configuration file
# -------------------------------------------------------------------

def EnigmaReadConfigiFile(filename):

    global abc
    global abclen
    global abcunk
    global date
    global line_count
    global plugs
    global reflst
    global rotors

    infile = open(filename,'r')

    for line in infile:

        line_count += 1

        line = line.strip()

        if not line:               # empty string (line)
            continue

        if re.match('^#',line):    # comment?
            continue

        x = line.split(',')

        # --- date file created

        if x[0] =='date':
            date = x[1]
            continue

        # --- alphabet length?

        if x[0] == 'len':          # length
            tf,i = ui.is_int(x[1])
            if tf:
                if i >= 0:
                    abclen = i
                    continue

        # --- unknown character?

        if x[0] == 'unk':          # unknown character
            abcunk = x[1]
            continue

        # --- alphabet?

        if x[0] == 'abc':          # alphabet
            abc.append(x[2])
            continue

        # --- plug?

        if x[0] == 'plug':         # plugboard
            plugs.append(x[1])
            continue

        # ---- reflector?
        
        if x[0] == 'ref':          # reflector
            reflst.append(int(x[1]))
            continue

        # ---- rotor?

        if x[0] in rotors.keys():  # rotor
            rotors[x[0]].append(x[2])
            continue

        # ---- what?

        print()
        print(f'unknow line in config file (line={line_count})\n({line})')
        sys.exit()

    infile.close()

# -------------------------------------------------------------------
# ---- main
# -------------------------------------------------------------------

# ---- configuration file on command line?

if len(sys.argv) > 1:
    configfile = sys.argv[1]

if not os.path.exists(configfile):
    print()
    print(f'Can not find enigma configuration file ({configfile})') 
    print()
    sys.exit()

# ---- read config file

EnigmaReadConfigiFile(configfile)

# ---- now set abcidx

abcidx = list(range(abclen))

# ---- verify config file data

for r in rotors:
    if len(rotors[r]) != abclen:
        print()
        print('bad rotor list length (r)')
        sys.exit()
if len(abc) != abclen:
    print()
    print('bad abc list length\n(alphabet)')
    sys.exit()
if len(reflst) != abclen:
    print()
    print('bad reflector list length\n(reflector)')
    sys.exit()
for i in range(abclen):
    j = reflst[i]
    if reflst[j] != i:
        print(f'error in reflector pair i={i} j={j}')
        sys.exit()

# ---- print stats

print()
print(f'input    file: {configfile}')
print(f'date         : {date}')
print(f'alphabet  len: {len(abc)}')
print(f'  abclen     : {abclen}')
print(f'  abcunk     : {abcunk}')
print(f'rotor   count: {len(rotors)}')
for r in rotors.keys():
    print(f'  {r:5}   len: {len(rotors[r])}')
print(f'reflector len: {len(reflst)}')
print(f'plugs        : {len(plugs)}')
print(f'lines read   : {line_count}')
print()
