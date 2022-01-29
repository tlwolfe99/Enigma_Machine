#!/usr/bin/python3
# ===================================================================
# test the rotors, reflector and plugboard with and without
# rotor advance
# ===================================================================
# the user must advance to rotors with the "advance" command.
# they do not automatically advance.
# -------------------------------------------------------------------
# Note: because this is software and not hardware, we do some special
# "stuff" with characters not in the enigma machine's alphabet [A-Z].
# see the code/comments.
# ===================================================================

from EnigmaMachine import EnigmaMachine
import user_interface as ui
import re
import os
import sys

# -------------------------------------------------------------------
# ---- main
# -------------------------------------------------------------------

if __name__ == '__main__':

    # ---- start enigma machine simulation

    configfile = 'enigma_config.csv'

    if len(sys.argv) > 1:
        configfile = sys.argv[1]

    if not os.path.exists(configfile):
        print()
        print(f'Can not find enigma configuration file ({configfile})') 
        print()
        sys.exit()

    em = EnigmaMachine(configfile)

    # ---- user commands

    while True:

        print()
        print('Cmd: text,   advance, reset, set, display, stats')
        print('     autoon, autooff, subdebugon, subdebugoff')

        print()
        s = ui.get_user_input('Enter text: ')
        if not s:
           break

        # ---- display command

        if re.match('^display$',s):
            em.display_internal_state()
            continue

        # ---- display rotor stats command

        if re.match('^stats$',s):
            em.display_rotor_stats()
            continue

        # ---- advance the rotors

        if re.match('^advance$',s):
            em.advance_rotors()
            continue

        # ---- auto advance

        if re.match('^auto$',s):
            print()
            print(f'auto advance ({em.auto_advance_rotors})')
            continue

        if re.match('^auton$',s) or re.match('^autoon$',s):
            em.auto_advance_rotors = True
            continue

        if re.match('^autoff$',s) or re.match('^autooff$',s):
            em.auto_advance_rotors = False
            continue

        # ---- substitution debug

        if re.match('^subdebug$',s):
            print()
            print(f'substitution debug ({em.substitution_debug})')
            continue

        if re.match('^subdebugon$',s) or re.match('^subon$',s):
            em.substitution_debug = True
            continue

        if re.match('^subdebugoff$',s) or re.match('^suboff$',s):
            em.substitution_debug = False
            continue

        # ---- reset the rotors to the initial configuration

        if re.match('^reset$',s):
            em.reset()
            continue

        # ---- set rotor configuration support function

        def _get_set_rotor_configuration(r):

            while True:

                print()
                prompt = f'Enter {r} rotor\'s new config (name,start): '
                s = ui.get_user_input(prompt)
                if not s:
                    return None
 
                nn = s.split(',')
                if len(nn) != 2:
                    print()
                    print('bad input - try again')
                    continue

                nam = nn[0].strip().upper()
                num = nn[1].strip()

                if nam not in em.rotorkeys:
                    print()
                    print('bad input - try again')
                    continue
 
                tf,nnum = ui.is_int(num)
                if not tf or nnum < 0 or nnum > em.abclen-1:
                    print()
                    print('bad input - try again')
                    continue

                break
               
            return (nam,nnum)

        # ---- set the rotors to a specified configuration

        if re.match('^set$',s):

            names  = []
            starts = []

            x0 = _get_set_rotor_configuration('left')
            if x0 == None:
                print()
                print('No changees made')
                continue

            x1 = _get_set_rotor_configuration('middle')
            if x1 == None:
                print()
                print('No changees made')
                continue

            x2 = _get_set_rotor_configuration('right')
            if x2 == None:
                print()
                print('No changees made')
                continue

            names.append(x0[0])
            names.append(x1[0])
            names.append(x2[0])

            starts.append(x0[1])
            starts.append(x1[1])
            starts.append(x2[1])

            em.set(names,starts)

            continue


        # ---- convert the input text

        ss  = s.upper()              # convert input text to uppercase
        sss = []

        for c in ss:

            if c not in em.abc:
                print(f'char {c} not in alphabet ' +
                      f'- substituting {em.abcunk}')
                c = em.abcunk

            n = em.char_to_idx(c)    # convert a character to an index
            ##if n < 0:
            ##    continue

            newidx = em.substitution(n) # substitution cypher
    
            sss.append(em.abc[newidx])  # collect new characters into a list

        ssss = ''.join(sss)          # convert the list to a string

        print()
        print(f'{s} --> {ssss}')
