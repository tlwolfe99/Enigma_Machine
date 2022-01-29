#!/usr/bin/python3
# ===================================================================
# Use the enigma machine encrypt/decrypt a file
#
# Note: for simplicity sake, for this first program
#       a. any characters not in the enigma machine simulation's
#          alphabet, they will pass thru unchanged to the
#          output file.
#       b. the exception to rule "a" is that spaces will be
#          converted to an 'X'.
#       c. all characters in the input file will be converted to
#          uppercase before processing.
# ===================================================================

from EnigmaConfig import EnigmaConfig
from EnigmaMachine import EnigmaMachine
import copy
import os
import sys

inputfile  = 'xx.txt'
outputfile = 'yy.txt'
configfile = 'enigma_config_26.csv'

# -------------------------------------------------------------------
# ---- encrypt/decrypt character
# -------------------------------------------------------------------

def char_to_idx(c,abc):

    for i in range(len(abc)):
        if c == abc[i]:
            return i

    return -1

def convert_char(c,abc,abcunk):

    if c == ' ':
        c = abcunk

    c = c.upper()

    if c in em.abc:
        idx  = char_to_idx(c,abc)
        idxx = em.substitution(idx)
        ##print(f'c={c}  idx={idx}  idxx={idxx}')
        return (True,abc[idxx])
    
    return (False,c)

# -------------------------------------------------------------------
# ---- main
# -------------------------------------------------------------------

# ---- input/out file on command line?

l = len(sys.argv)

if l != 1:
    if l == 3:
        inputfile  = sys.argv[1]
        outputfile = sys.argv[2]
    else:
       print()
       print(f'wrong number ({l}) of command line arguments')
       print()
       sys.exit()

# ---- create an enigma machine object

em = EnigmaMachine(configfile)

# ---- process input/output files

total_chars     = 0
line_count      = 0
chars_converted = 0

inFile = open(inputfile,'r')
outfile= open(outputfile,'w')

for line in inFile:

    line_count += 1

    total_chars += len(line)

    lst_in = list(line)

    lst_out = copy.copy(lst_in)

    ##print(f'lst_in = {lst_in}')
    ##print(f'lst_out= {lst_out}')

    for i in range(len(lst_in)):
        c = lst_in[i]
        tf,cc = convert_char(c,em.abc,em.abcunk)
        lst_out[i] = cc

        if tf:
            chars_converted += 1

    str_out = ''.join(lst_out)

    outfile.write(str_out)

inFile.close()
outfile.close()

# ---- display processing stats

print()
print(f'In file        : {inputfile}')
print(f'Out file       : {outputfile}')
print(f'lines read     : {line_count}')
print(f'total chars    : {total_chars}')
print(f'chars converted: {chars_converted}')
print()
