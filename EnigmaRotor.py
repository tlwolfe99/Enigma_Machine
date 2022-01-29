# ===================================================================
# Enigma Machine Simulation - rotor
# ===================================================================

from EnigmaConfig import EnigmaConfig
import EnigmaUtils as util
import copy

class EnigmaRotor():

    # ---------------------------------------------------------------
    # ---- initialize rotor object
    # ---------------------------------------------------------------
    # ---- abc             alphabet list
    # ---- abclen          alphabet list length
    # ---- abcunk          unknown character substitute
    # ---- rotors          configuration file dictionary of
    # ----                     rotor lists (I,II,...,VIII)
    # ---- rotor_name      rotor name (from rotors)
    # ---- rotor_start     rotor start position (idx=0)
    # ---- rotor_count     rotation/advancement count
    # ---- lst             randomized list of indexes from
    # ----                   configuration file 
    # ----                 (associated with the alphabet)
    # ---- lstlen          length, lst
    # ---- ltor            left-to-right substitution list
    # ---- rtol            right-to-left substitution list
    #----------------------------------------------------------------
    def __init__(self,config,rotor_name,rotor_start):

        self.abc         = config.abc
        self.abcidx      = config.abcidx
        self.abclen      = config.abclen
        self.abcunk      = config.abcunk
        self.rotors      = config.rotors
        self.rotor_name  = rotor_name
        self.rotor_start = rotor_start
        self.rotor_count = 0
        self.lst         = []
        self.lstlen      = []
        self.rtol        = []
        self.ltor        = []

        self.reset(rotor_name,rotor_start)

    # ---------------------------------------------------------------
    # ---- character substitution right-to-left
    # ---------------------------------------------------------------
    def rtol_substitution(self,idx):
        return self.rtol[idx]

    # ---------------------------------------------------------------
    # ---- character substitution left-to-right
    # ---------------------------------------------------------------
    def ltor_substitution(self,idx):
        return self.ltor[idx]

    # ---------------------------------------------------------------
    # ---- reset rotor starting position
    # ---------------------------------------------------------------
    def reset(self,rotor_name,rotor_start):

        self.rotor_name  = rotor_name
        self.rotor_start = rotor_start
        self.rotor_count = 0

        # ---- fill rotor randomized substitution list

        self.lst    = self.rotors[rotor_name]  # indexes list
        self.lstlen = len(self.lst)            # indexes list length

        # ---- fill in the rtol randomized substitution list

        self.rtol = [None] * self.lstlen

        for i in range(self.lstlen):
            self.rtol[i] = self.lst[i]

        # --- shift rtol list so rotor_start is index 0

        if rotor_start >= 0:
           self.rtol = self._shift_rotor(rotor_start,self.rtol)

        # ---- sync rotor's ltor list with it's rotl list

        self.ltor = [None] * self.lstlen

        for i in range(self.abclen):
            self.ltor[self.rtol[i]] = i

    # ---------------------------------------------------------------
    # ---- helper function: set rotor configuration
    # ---------------------------------------------------------------
    def _shift_rotor(self,idx,lst):

        # ---- create new list

        new_lst = [-1] * self.lstlen  # set everything to -1

        # --- copy lower half of original list to new list

        i = 0                         # new list index

        for j in range(idx,self.lstlen):
            new_lst[i] = lst[j]   # copy original list to new list
            i += 1                # increment new list index

        # ---- copy upper part of original list to new list

        for j in range(0,idx):
            new_lst[i] = lst[j]   # copy original list to new list
            i += 1                # increment new list index

        ##print(f'new lst: {self.rotor_name} {self.rotor_start}')
        ##print(f'old={lst} new={new_lst}')

        return new_lst

    # ---------------------------------------------------------------
    # ---- display rotor internals
    # ----------------------------------------------------------------
    def display(self,title=None,all=True):
        print()
        for k in self.rotors.keys():
            print(f'{k:>4} {self.rotors[k]}')
        print()
        if title:
            print(title)
        if all:
            print('-lst-   l-to-r    r-to-l')
            for i in range(self.lstlen):
                print(f'{i:2} {self.lst[i]:<2}  ' +
                      f'{i:>2} -> {self.ltor[i]:<2}  ' +
                      f'{self.rtol[i]:>2} <- {i:<2}')
        print(f'rotor_name  = {self.rotor_name}')
        print(f'rotor_start = {self.rotor_start}') 
        print(f'rotor_count = {self.rotor_count}')
