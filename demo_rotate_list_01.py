#!/usr/bin/python3
# ===================================================================
# rotate a python list one position
# note: this code is insufficient for enigma machine rotor rotation
#       remember, the list index and its list value represents
#       an electronic circuit (wire). the wire starts and an index
#       and ends a specific number of indexes away.
#       the wire's end point (list values) must also be moved.
# ===================================================================

lst    = ['a','b','c','d','e','f']  # list
lstlen = len(lst)                   # list length

print()
print(lst)

for i in range(lstlen):

    print(f'[{i:>2}]  {lst})   # display initial list

    # ---- move list values up one position

    tmp = lst[0]

    for i in range(lstlen-1):
        lst[i] = lst[i+1]

    lst[-1] = tmp

    print(f'[{i:>2}]  {lst})   # display rotated list
