#!/usr/bin/python3
# ===================================================================
# rotate a python list one position
# (save the rotated lists and then dislay them at the end)
# 
# can you think of a way to rotate a list with the mod operator?
# ===================================================================

import copy

lst    = ['a','b','c','d','e','f']  # list
lsts   = []                         # list of lists

# ---- return a new rotated (one position) list
def rotate_list(lst):
    newlst = copy.copy(lst)
    tmp = newlst[0]
    for i in range(len(newlst)-1):
        newlst[i] = newlst[i+1]
    newlst[-1] = tmp
    return newlst

# ---- create list of lists

lsts.append(lst)    # starting list

print(lsts)
print(lsts[-1])

for _ in range(10):
    rotlst = rotate_list(lsts[-1])
    lsts.append(rotlst)

# ---- display lists

print()
print('Rotate a list one position at a time')

print()
for i in range(len(lst)):
    for j in range(len(lsts)):
        print(f'{lsts[j][i]}  ',end='')
    print()
print()
