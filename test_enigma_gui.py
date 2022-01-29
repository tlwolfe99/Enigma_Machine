#!/usr/bin/python3
# ===================================================================
# test Enigma Machine simple GUI
# ===================================================================

from enigma_gui import enigma_gui
from EnigmaConfig import EnigmaConfig
from EnigmaMachine import EnigmaMachine
import PySimpleGUI as sg
import os
import re
import sys

# ---- configuration file

configfile = 'enigma_config.csv'

if len(sys.argv) > 1:
     configfile = sys.argv[1]

if not os.path.exists(configfile):
    print()
    print(f'Can not find enigma configuration file ({configfile})') 
    print()
    sys.exit()

# ---- create enigma machine simulation

em = EnigmaMachine(configfile)

# ---- create a GUI window

win,tsize = enigma_gui(em.config)

# ---- alphabet to index

def _char_to_idx(c,abc):
    for i in range(len(abc)):
        if abc[i] == c:
            return i
    return 0

# ---- event loop
x = ''

while(True):

    event,values = win.read()

    ##print('-----------------------------------------')
    ##print(f'event={event}')
    ##print(values)
    ##print('-----------------------------------------')

    # ---- keypress

    if event in em.config.abc:

        if len(x) < tsize:
            x = x + event
            win['-IN-'].update(x)
        continue

    # ---- exit program

    if event in ('Exit',sg.WIN_CLOSED):
        break

    # ---- reset rotors

    if event == 'Reset Rotors':
        x = ''
        win['-IN-'].update(x)
        win['-OUT-'].update(x)
        em.reset()
        continue

    # ---- set rotors

    if event == 'Set Rotors':

        win['-IN-'].update('')
        win['-OUT-'].update('')

        rnam = values['-RROTOR-']
        rpos = values['-RPOSITION-']
        ridx = _char_to_idx(rpos,em.abc)

        mnam = values['-MROTOR-']
        mpos = values['-MPOSITION-']
        midx = _char_to_idx(mpos,em.abc)

        lnam = values['-LROTOR-']
        lpos = values['-LPOSITION-']
        lidx = _char_to_idx(lpos,em.abc)

        nam = [lnam,mnam,rnam]
        pos = [lidx,midx,ridx]
        print(f'names: {nam}  starts: {pos}')
        continue

    # ---- encrypt/decrypt input data

    if event == 'Encrypt/Decrypt':
        continue

    # ---- enigma machine display function

    if event == 'Display':
        em.display_internal_state()
        continue

    # ---- enigma machine display rotor stats

    if event == 'Stats':
        em.display_rotor_stats()
        continue
        

win.close()
print()
