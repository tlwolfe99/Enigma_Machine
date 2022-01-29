#!/usr/bin/python3
# ===================================================================
# test: list2 = list1
# ===================================================================

def list_info(name,lst):
    ##print(f'type   = {type(lst)}')
    print(f'id     = {id(lst)}')
    print(f'{name:6} = {lst}')

def test_func(list1):
    print('\ntest func')
    list2 = list1
    print('change list2 ([0] = 9)')
    list2[0] = 9
    print()
    list_info('list1',list1)
    list_info('list2',list2)


print('\nmain')

list1 = [0,1,2,3,4,5]

list_info('list1',list1)

test_func(list1)

print('\nmain')
list_info('list1',list1)
