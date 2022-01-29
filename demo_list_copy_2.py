#!/usr/bin/python3
# ===================================================================
# test: copy shalow list
#       list1 = copy.copy(list1) and copy.deepcopy(list1) 
# ===================================================================

import copy

print('\n---- original: list1')
list1 = [0,1,2,3,4,5]
print(f'list1    id = {id(list1)}  list1={list1}') 
print(f'list1[0] id = {id(list1[0])}')

print('\n---- copy: list2 = copy.copy(list1)')
list2 = copy.copy(list1)
print('---- modify: list2[0] = "A"')
list2[0] = 'A'
print(f'list2    id = {id(list2)}  list2={list2}')
print(f'list2[0] id = {id(list2[0])}')
print(f'list1    id = {id(list1)}  list1={list1}')
print(f'list1[0] id = {id(list1[0])}')

print('\n---- deepcopy: list3 = copy.deepcopy(list1)')
list3 = copy.deepcopy(list1)
print('---- modify: list3[0] = "B"')
list3[0] = 'B'
print(f'list3    id = {id(list3)}  list3={list3}')
print(f'list3[0] id = {id(list3[0])}')
print(f'list1    id = {id(list1)}  list1={list1}')
print(f'list1[0] id = {id(list1[0])}')
