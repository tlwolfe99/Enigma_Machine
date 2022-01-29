# ===================================================================
# Enigma Machine Simulation - read/process configuration file
# ===================================================================

from datetime import date
import user_interface as ui
import copy
import re
import sys

# --------------------------------------------------------------------
# ---- namespace for enigma simulation runtime configuration
# --------------------------------------------------------------------

class EnigmaConfig():

    def __init__(self,filename):

        # ---- rotor dictionary and keys
        self.rotors     = { 'I':[], 'II':[], 'III':[],   'IV':[],
                            'V':[], 'VI':[], 'VII':[], 'VIII':[] }

        self.rotorkeys = list(self.rotors.keys())

        self.abc        = []                       # alphabet list
        self.abclen     = 0                        # abc list length
        self.abcidx     = []                       # list of alphabet
                                                   #   indexes
        self.configfile = filename                 # configuration
                                                   #   file
        self.line_count = 0                        # line count read
                                                   #   from config file
        self.plugs      = []                       # plugboard pairs
        self.pglst      = []                       # plugboard list
        self.reflst     = []                       # reflector list
        self.date       = date.today()             # config file date

        # ---- default enigma machine rotor configuration

        self.default_rotor_names = ['III','II','I']
        self.default_rotor_starts= [2,1,0]

        # ---- create an empty configuration

        if not filename:
            return

        # ---- read/process configuration file

        fh = open(filename,'r')

        for line in fh:

            self.line_count += 1

            line = line.strip()

            if not line:               # empty string (line)
                continue

            if re.match('^#',line):         # comment
                continue

            x = line.split(',')

            # --- date file created

            if x[0] =='date':               # date
                self.date = x[1]
                continue

            # --- alphabet length?

            if x[0] == 'len':               # alphabet length
                tf,i = ui.is_int(x[1])
                if tf:
                    if i >= 0:
                        self.abclen = i
                        continue

            if x[0] == 'unk':               # substitute for unknown
                                            #   character
                self.abcunk = x[1]
                continue

            # --- alphabet?

            if x[0] == 'abc':               # alphabet
                if x[2] == '':              # special case for
                    x[2] = ' '              #   space character
                self.abc.append(x[2])
                continue

            # --- plug?

            if x[0] == 'plug':              # plugboard
                self.plugs.append(x[1])
                continue

            # ---- reflector?
        
            if x[0] == 'ref':               # reflector
                self.reflst.append(int(x[2]))
                continue

            # ---- rotor?

            if x[0] in self.rotors.keys():  # rotor
                tf,i = ui.is_int(x[2])
                if tf:
                    if i >= 0:
                        self.rotors[x[0]].append(int(x[2]))
                        continue

            # ---- what?

            print()
            print('unknown line in config file ' +
                 f'line={line_count})\n({line})')
            sys.exit()

        fh.close()

        # ---- verify config file data

        for r in self.rotors:
            if len(self.rotors[r]) != self.abclen:
                print()
                print(f'bad rotor list length (r)')
                sys.exit()
        if len(self.abc) != self.abclen:
            print()
            print('bad abc list length\n(alphabet)')
            sys.exit()
        if len(self.reflst) != self.abclen:
            print()
            print('bad reflector list length\n(reflector)')
            sys.exit()
        for i in range(self.abclen):
            j = self.reflst[i]
            if self.reflst[j] != i:
                print(f'error in reflector pair i={i} j={j}')
                sys.exit()

        # ---- now set abcidx (alphabet index list)

        self.abcidx = list(range(self.abclen))

        # ---- now create plugboard

        self.create_plugboard()

    # ---------------------------------------------------------------
    # ---- helper function: convert character to index
    # ---------------------------------------------------------------

    def _char_to_index(self,c):
        for i in range(len(self.abc)):
            if c == self.abc[i]:
                return i
        print()
        print(f'character c not found in alphabet')
        sys.exit()

    # ---------------------------------------------------------------
    # ---- create plugboard (list)
    # ---------------------------------------------------------------

    def create_plugboard(self):

        used_chars = []

        self.pglst = list(range(self.abclen))

        for cc in self.plugs:

            # --- error check

            if len(cc) != 2 or cc[0] == cc[1] or \
                cc[0] in used_chars or \
                cc[1] in used_chars or \
                cc[0] not in self.abc or \
                cc[1] not in self.abc:
                print()
                print(f' error in plugboard pair ({cc})')
                sys.exit()

            used_chars.append(cc[0])
            used_chars.append(cc[1])

            idx0 = self._char_to_index(cc[0])
            idx1 = self._char_to_index(cc[1])

            self.pglst[idx0] = idx1
            self.pglst[idx1] = idx0

    # ---------------------------------------------------------------
    # ---- display EnigmaConfig internals
    # ---------------------------------------------------------------

    def display_config(self):
        self.display_stats()

    def display_stats(self):
        print()
        print(f'config   file: {self.configfile}')
        print(f'date         : {self.date}')
        print(f'lines read   : {self.line_count}')
        print(f'alphabet  len: {len(self.abc)}')
        print(f'  abclen     : {self.abclen}')
        print(f'  abcunk     : {self.abcunk}')
        print(f'rotor   count: {len(self.rotors)}')
        for r in self.rotors.keys():
            print(f'  {r:5}   len: {len(self.rotors[r])}')
        print(f'reflector len: {len(self.reflst)}')
        print(f'plugs        : {len(self.plugs)}')
        for p in self.plugs:
            print(f'  ({p})')
        ##for idx in range(len(self.pglst)):
        ##    print(f'  {idx:>2} --> {self.pglst[idx]:<2}  i' +
        ##          f'({self.abc[idx]})')
        print()
