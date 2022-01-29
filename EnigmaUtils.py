# ===================================================================
# Enigma Machine Simulation - support functions
# ===================================================================

import copy
from   datetime import date
import re
import sys
import random
import user_interface as ui

# -------------------------------------------------------------------
# ---- create a randomize rotor list
# ---- 1. input list must contain a least two values
# ---- 2. input list must contain an even number of values
# ---- 3. this function ensures every list-value will end up in a
# ----    different location (list-index) in the randomized list.
# ----    different locations are required by the enigma machine.
# ----    we are simulating electric circuits. IN can not be the
# ----    same wire as OUT. See the electric circuit diagram
# ----    elsewhere.
# ---- 4. no list-value in the list is allowed to be randomized
# ----    to itself (ie. lst[10] can not be 10)
# -------------------------------------------------------------------

def create_randomized_rotor_list(lst, debug=False):

    ranlst = copy.deepcopy(lst)

    i = 0                     # ranlst list index
    s = 1                     # start of random range
    e = len(ranlst)-1         # end   of random range

    if debug:
        print(f'ranlst: {ranlst}  (original list)')

    while s < e:

        j = random.randint(s,e)

        tmp = ranlst[i]
        ranlst[i] = ranlst[j]
        ranlst[j] = tmp

        if debug:
            print(f'ranlst: {ranlst}')

        i += 1
        s += 1

    # ---- make sure the last two don't encode themselves

    tmp        = ranlst[-1]
    ranlst[-1] = ranlst[-2]
    ranlst[-2] = tmp

    if debug:
        print(f'ranlst: {ranlst}  (last two swapped list)')

    # ---- return the randomized list

    return ranlst

# -------------------------------------------------------------------
# ---- create a randomize reflector list
# ---- 1. input list must contain a least two values
# ---- 2. input list must contain an even number of values
# ---- 3. this function ensures every list element is paired with
# ----    another list element. Each pair is unique and reference
# ----    each other (i.e. lst[6] = 10 and lst[10] = 6)
# -------------------------------------------------------------------

def create_randomized_reflector_list(lst, debug=False):

    def _pop_random(lst):
        idx = random.randrange(0,len(lst))
        return lst.pop(idx)

    cpylst = copy.deepcopy(lst)

    reflst = [None] * len(lst)

    while cpylst:
        idx1 = _pop_random(cpylst)
        idx2 = _pop_random(cpylst)
        reflst[idx1] = idx2
        reflst[idx2] = idx1

    return reflst
