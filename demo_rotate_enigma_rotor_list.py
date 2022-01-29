#!/usr/bin/python3
# ===================================================================
# use a python list to simulate rotating an enigma rotor
# the rotor is a hard wired substitution cipher and rotates "upward"
# or "forward" one position (a -> b -> c -> ...)
#
# a list index is an index into a alphabet list used to translate
# between indexes and alphabetic letters
#
# the list index is the IN character and the list value is the index
# of the OUT character
#
# ---- pattern the code is trying to duplicate ----------------------
#
#    [0]     [1]     [2]     [3]     [4]
#   IN OUT  IN OUT  IN OUT  IN OUT  IN OUT
#   0 -> 2  0 -> 2  0 -> 3  0 -> 1  0 -> 2 
#   1 -> 3  1 -> 0  1 -> 2  1 -> 3  1 -> 3
#   2 -> 1  2 -> 3  2 -> 0  2 -> 0  2 -> 1
#   3 -> 0  3 -> 1  3 -> 1  3 -> 2  3 -> 0
#
# ===================================================================

abc    = ['A','B','C','D']     # alphabet
lst    = [2,3,1,0]             # randomized list       
lstlen = len(lst)              # list length

# ---- display the current index list

def display_list(n,lst,lstlen,abc):
    print(f'[{n}] {lst}  [',end='')
    for i in range(lstlen):
        if i != 0: print(',',end='')
        print(f' {abc[lst[i]]}',end='')
    print(' ]')


# ---- main

print()
display_list(0,lst,lstlen,abc)

for j in range(1,8):           # rotate and display rotor list

    # ---- rotate the list (enigma rotor)
    # ---- move the list values up one position (a->b)
    # ---- modify the list value to be the index of the OUT
    # ---- character

    tmp = lst[0]

    for i in range(lstlen-1):
       lst[i] = (lst[i+1] - 1) % lstlen

    lst[-1] = (tmp-1) % lstlen

    if j % lstlen == 0:
        print()
    display_list(j,lst,lstlen,abc)

