# ===================================================================
# test the enigma machine simulation with and without rotor advance
# ===================================================================
# the user can advance the rotors with the "advance" command.
# -------------------------------------------------------------------
# Note: because this is software, we do some special "stuff" with
# characters not in the enigma machine's alphabet [A-Z]. see the
# code/comments.
# ===================================================================

from EnigmaConfig    import EnigmaConfig
from EnigmaRotor     import EnigmaRotor
import EnigmaUtils
import user_interface as ui
import copy
import re
import sys


class EnigmaMachine:

    # ---------------------------------------------------------------
    # ---- initialize object
    # ---------------------------------------------------------------
    def __init__(self,configfile):

        # ---- enigma machine configuration

        self.config = EnigmaConfig(configfile)

        # ---- enigma machine alphabet

        self.abc    = self.config.abc
        self.abcidx = self.config.abcidx
        self.abclen = self.config.abclen
        self.abcunk = self.config.abcunk

        self.rotorkeys = self.config.rotorkeys

        # ---- left rotor, middle rotor, right rotor,
        # ---- reflector, plugboard

        self.lr = EnigmaRotor(self.config,
                self.config.default_rotor_names[0],
                self.config.default_rotor_starts[0])
        self.mr = EnigmaRotor(self.config,
                self.config.default_rotor_names[1],
                self.config.default_rotor_starts[1])
        self.rr = EnigmaRotor(self.config,
                self.config.default_rotor_names[2],
                self.config.default_rotor_starts[2])
        self.rf = copy.deepcopy(self.config.reflst)
        self.pg = copy.deepcopy(self.config.pglst)

        # ---- automatic advance rotors

        self.auto_advance_rotors = True 

        # ---- substitution debug messages

        self.substitution_debug = False

    # ---------------------------------------------------------------
    # ---- display internal state of enigma machine
    # ---------------------------------------------------------------
    def display_internal_state(self):
        print()
        print('                    -- Left Rotor --- ' +
              '-- Middle Rotor - -- Right Rotor --')
        print('plugboard reflector  ' +
              'l-to-r   r-to-l   l-to-r   r-to-l   l-to-r   r-to-l')
        print('--------- --------- -------- -------- ' +
              '-------- -------- -------- --------')
        for i in range(self.abclen):
             print(f'{i:>2} -> {self.pg[i]:<2}  ' +
                   f'{i:>2} -> {self.rf[i]:<2}  ' +
                   f'{i:>2} -> {self.lr.ltor[i]:<2} ' +
                   f'{self.lr.rtol[i]:>2} <- {i:<2} ' +
                   f'{i:>2} -> {self.mr.ltor[i]:<2} ' +
                   f'{self.mr.rtol[i]:>2} <- {i:<2} ' +
                   f'{i:>2} -> {self.rr.ltor[i]:<2} ' +
                   f'{self.rr.rtol[i]:>2} <- {i:<2}')
        print(f'---- auto advance rotors ({self.auto_advance_rotors})')
        print(f'---- right  start {self.rr.rotor_start:<2} ' +
              f'rotor {self.rr.rotor_name:<4} ' +
              f'count {self.rr.rotor_count}')
        print(f'---- middle start {self.mr.rotor_start:<2} ' +
              f'rotor {self.mr.rotor_name:<4} ' +
              f'count {self.mr.rotor_count}')
        print(f'---  left   start {self.lr.rotor_start:<2} ' +
              f'rotor {self.lr.rotor_name:<4} ' +
              f'count {self.lr.rotor_count}')
        return

    # ---------------------------------------------------------------
    # ---- display rotor stats of enigma machine
    # ---------------------------------------------------------------
    def display_rotor_stats(self):
        print()
        print(f'auto advance rotors ({self.auto_advance_rotors})')
        print(f'right  start {self.rr.rotor_start:<2} ' +
              f'rotor {self.rr.rotor_name:<4} ' +
              f'count {self.rr.rotor_count}')
        print(f'middle start {self.mr.rotor_start:<2} ' +
              f'rotor {self.mr.rotor_name:<4} ' +
              f'count {self.mr.rotor_count}')
        print(f'left   start {self.lr.rotor_start:<2} ' +
              f'rotor {self.lr.rotor_name:<4} ' +
              f'count {self.lr.rotor_count}')
        return

    # ---------------------------------------------------------------
    # ---- convert character to index
    # ---------------------------------------------------------------
    def char_to_idx(self,c):
        if c in self.abc:
            for i in range(self.abclen):
                if self.abc[i] == c:
                    return i
        return -1

    # ---------------------------------------------------------------
    # ---- convert index to character
    # ---------------------------------------------------------------
    def idx_to_char(self,idx):
        return self.abc[idx]
         
    # ---------------------------------------------------------------
    # ---- character in alphabet
    # ---------------------------------------------------------------
    def char_in_alphabet(self,c):
        if c in self.abc:
            return True
        return False

    # ---------------------------------------------------------------
    # ---- advance the rotors one position
    # ---- advance each rotor until it makes a complete revolution
    # ----   then start over again
    # ---- note: tf is a true/false flag
    # ----       True  have completed a full rotation
    # ----       False have not completed a complete full rotation
    # ---------------------------------------------------------------
    def advance_rotors(self):

        tf = self.advance(self.rr)           # right rotor
        if tf:
            tf = self.advance(self.mr)       # middle rotor
            if tf:
                tf = self.advance(self.lr)   # left rotor
        return

    # ---------------------------------------------------------------
    # ---- advance a rotor
    # ---- return:
    # ----     True  have completed a full rotation
    # ----     False have not completed a complete full rotation
    # ---------------------------------------------------------------
    def advance(self,r):

        # ---- advance rotor's rtol list

        rtollen = len(r.rtol)

        tmp = r.rtol[0]

        for i in range(rtollen-1):
            r.rtol[i] = (r.rtol[i+1] - 1) % rtollen

        r.rtol[-1] = (tmp-1) % rtollen

        # ---- sync rotor's ltor list with its rotl list

        for i in range(rtollen):
            r.ltor[r.rtol[i]] = i  

        # ---- check for a complete rotation of the rotor
        # ---- (end of list)

        r.rotor_count += 1
        if not r.rotor_count < rtollen:
            r.rotor_count = 0
            return True
        return False

    # ---------------------------------------------------------------
    # ---- reset the internal state to the initial configuration
    # ---------------------------------------------------------------
    def reset(self):

        self.lr = EnigmaRotor(self.config,
                self.config.default_rotor_names[0],
                self.config.default_rotor_starts[0])
        self.mr = EnigmaRotor(self.config,
                self.config.default_rotor_names[1],
                self.config.default_rotor_starts[1])
        self.rr = EnigmaRotor(self.config,
                self.config.default_rotor_names[2],
                self.config.default_rotor_starts[2])

        self.lr.rotor_count = 0
        self.mr.rotor_count = 0
        self.rr.rotor_count = 0

        return

    # ---------------------------------------------------------------
    # ---- set rotor configuration
    # ---- the initial rotor configuration is still available
    # ---- using reset_initial_state function 
    # ---------------------------------------------------------------
    def set(self,names,starts):

        # --- verify input lists

        if len(names)  != 3 or len(starts) != 3:
               print()
               print('internal error - bad set rotor comfiguration ' +
                     'names or starts list size')
               print(f'({names}) ({starts})')
               print()
               sys.exit()

        for i in range(3):
            if names[i] not in self.rotorkeys: 
               print()
               print('internal error - bad set rotor comfiguration ' +
                     'rotor name')
               print(f'({names})')
               print()
               sys.exit()

        for s in range(3):
            if s< 0 or s >self.config.abclen-1:
               print()
               print('internal error - bad set rotor comfiguration ' +
                     'start position')
               print(f'({starts})')
               print()
               sys.exit()

        # ---- set rotor configuration

        self.lr = EnigmaRotor(self.config,names[0],starts[0])
        self.mr = EnigmaRotor(self.config,names[1],starts[1])
        self.rr = EnigmaRotor(self.config,names[2],starts[2])

        self.lr.rotor_count = 0
        self.mr.rotor_count = 0
        self.rr.rotor_count = 0

        return


    # ---------------------------------------------------------------
    # ---- change auto advance
    # ---------------------------------------------------------------

    def auto_advance_on(self):
        self.auto_advance_rotors = True
        return True

    def auto_advance_off(self):
        self.auto_advance_rotors = False
        return False

    def auto_advance_state(self):
        return auto_advance_rotors

    # ---------------------------------------------------------------
    # ---- change substitution debug
    # ---------------------------------------------------------------

    def sub_debug_on(self):
        self.substitution_debug = True
        return True

    def sub_debug_off(self):
        self.substitution_debug = False
        return False

    def sub_debug_state(self):
        return self.substitution_debug 

    # ---------------------------------------------------------------
    # ---- substitute character
    # ---------------------------------------------------------------
    def substitution(self,idx):

        idx1 = self.pg[idx]                      # plugboard
        idx2 = self.rr.rtol_substitution(idx1)
        idx3 = self.mr.rtol_substitution(idx2)
        idx4 = self.lr.rtol_substitution(idx3)
        idx5 = self.rf[idx4]                     # reflector
        idx6 = self.lr.ltor_substitution(idx5)
        idx7 = self.mr.ltor_substitution(idx6)
        idx8 = self.rr.ltor_substitution(idx7)
        idx9 = self.pg[idx8]                      # plugboard

        if self.substitution_debug:
            print(f'{idx} --> ',end='')
            print(f'{idx1} --> ',end='')
            print(f'{idx2} --> ',end='')
            print(f'{idx3} --> ',end='')
            print(f'{idx4} --> ',end='')
            print(f'{idx5} --> ',end='')
            print(f'{idx6} --> ',end='')
            print(f'{idx7} --> ',end='')
            print(f'{idx8} --> ',end='')
            print(f'{idx9}')

            print(f'{self.abc[idx]} --> ',end='')
            print(f'{self.abc[idx1]} --> ',end='')
            print(f'{self.abc[idx2]} --> ',end='')
            print(f'{self.abc[idx3]} --> ',end='')
            print(f'{self.abc[idx4]} --> ',end='')
            print(f'{self.abc[idx5]} --> ',end='')
            print(f'{self.abc[idx6]} --> ',end='')
            print(f'{self.abc[idx7]} --> ',end='')
            print(f'{self.abc[idx8]} --> ',end='')
            print(f'{self.abc[idx9]}')
            print(f'[{idx} ({self.abc[idx]})]  -->  ' +
                  f'[{idx8} ({self.abc[idx9]})]')

        if self.auto_advance_rotors:
            self.advance_rotors()

        return idx9

