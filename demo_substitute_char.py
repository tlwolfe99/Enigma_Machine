#!/usr/bin/python3
# ===================================================================
#
# ===================================================================


abc    = [ 'A','B','C','D','E','F','G','H' ]  # alphabet

abcunk = 'X'                   # substutue for unknown characters
txt    = 'abcz87d'             # test string 
txtlst = list(txt)             # convert test string to a list

print()
print(f'txt    = {txt}')
print(f'txtlst = {txtlst}')

# ---- substitute (abcunk) for characters not in alphabet (abc)

for i in range(len(txtlst)):

    # ---- character in alphabet? no, substitute abcunk
    if txtlst[i].upper() not in abc:
        txtlst[i] = abcunk

newtxt = ''.join(txtlst)       # convert list to a string

print(f'newtxt = {newtxt}')
