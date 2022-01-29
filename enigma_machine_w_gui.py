#!/usr/bin/python3
# ===================================================================
# Enigma machine simulation and a GUI
# ===================================================================

from enigma_gui import enigma_gui
from EnigmaConfig import EnigmaConfig
from EnigmaMachine import EnigmaMachine
import PySimpleGUI as sg
import os
import re
import sys

# -------------------------------------------------------------------
# ---- configuration
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

# ---- create an enigma machine object

em = EnigmaMachine(configfile)

# ---- create a GUI window

win,tsize = enigma_gui(em.config)

# -------------------------------------------------------------------
# ----event loop 
# -------------------------------------------------------------------

# ---- alphabet to index support function

def _char_to_idx(c,abc):
    for i in range(len(abc)):
        if abc[i] == c:
            return i
    return 0


lst_in  = ''
lst_out = ''

while(True):

    # ---- wait on an event

    event,values = win.read()

    ##print()
    ##print(f'event = {event}')
    ##print(f'values= {values}')
    ##print()

    # ---- event: exit program

    if event in ('Exit',sg.WIN_CLOSED):
        break

    # ---- event: single character

    if len(event) == 1:
        if event not in em.config.abc:
            print()
            print('internal error - do not recognize event ' +
                 f'({event}) - end program')
            print()
            sys.exit()

        lst_in = lst_in + event
        if len(lst_in) > tsize-1:
            win['-IN-'].update('text buffer overflow')
            win['-OUT-'].update('text buffer overflow')
            continue
        win['-IN-'].update(lst_in)

        idx_in = em.char_to_idx(event)
        idx_out = em.substitution(idx_in)
        lst_out = lst_out + em.idx_to_char(idx_out)
        win['-OUT-'].update(lst_out)

        continue

    # ---- event: reset rotors

    if event == 'Reset Rotors':
        lst_in  = ''
        lst_out = ''
        win['-IN-'].update('')
        win['-OUT-'].update('')
        em.reset()
        continue

    # ---- set rotors

    if event == 'Set Rotors':
 
        lst_in  = ''
        lst_out = ''
        win['-IN-'].update('')
        win['-OUT-'].update('')

        rnam = values['-RROTOR-']
        rpos = values['-RPOSITION-'].upper()
        ridx = _char_to_idx(rpos,em.abc)

        mnam = values['-MROTOR-']
        mpos = values['-MPOSITION-'].upper()
        midx = _char_to_idx(mpos,em.abc)

        lnam = values['-LROTOR-']
        lpos = values['-LPOSITION-'].upper()
        lidx = _char_to_idx(lpos,em.abc)

        nam = [lnam,mnam,rnam]
        pos = [lidx,midx,ridx]
        em.set(nam,pos)
        continue


    # ---- event: clear encrypt/decrypt buffers

    if event == 'Clear Buffer':
        lst_in  = ''
        lst_out = ''
        win['-IN-'].update('')
        win['-OUT-'].update('')
        continue

    # ---- event: display (enigma machine internals)

    if event == 'Display':
        em.display_internal_state()
        continue

    # ---- event: stats (enigma machine rotor info) 

    if event == 'Stats':
        em.display_rotor_stats()
        continue

    # ---- event: auto advance on

    if event == 'Auto Advance On':
        em.auto_advance_on()
        continue

    # ---- event: auto advance off

    if event == 'Auto Advance Off':
        em.auto_advance_off()
        continue

    # ---- event: substitution debug on

    if event == 'Sub Debug On':
        em.sub_debug_on()
        continue

    # ---- event: substitution debug off

    if event == 'Sub Debug Off':
        em.sub_debug_off()
        continue

win.close()
print()
