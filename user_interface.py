#! /usr/bin/python3
# ===================================================================
# command line user interface functions
# (see the example code at the end of this file)
# ===================================================================

import os
import sys
import platform

# -------------------------------------------------------------------
# ----running Python3?
# -------------------------------------------------------------------

def running_python3():
    if sys.version_info[0] == 3:
        return True
    return False

# -------------------------------------------------------------------
# ---- prompt the user for input
# -------------------------------------------------------------------

def get_user_input(prompt):
    return input(prompt).strip()

# -------------------------------------------------------------------
# ---- pause program
# -------------------------------------------------------------------

def pause():
    print()
    get_user_input('Press enter to continue ')

# -------------------------------------------------------------------
# ---- clear the terminal screen (window)
# -------------------------------------------------------------------

def clear_screen():
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('clear')
    else:
        os.system('cls')

# -------------------------------------------------------------------
# ---- Function: convert a string to a float
# -------------------------------------------------------------------

def is_float(s):
    try:
        n = float(s)
        return (True,n)
    except:
        return (False,0.0)

# -------------------------------------------------------------------
# ---- Function: convert a string to an int
# -------------------------------------------------------------------

def is_int(s):
    try:
        n = int(s)
        return (True,n)
    except:
        return (False,0)

def is_integer(s):
    try:
        n = int(s)
        return (True,n)
    except:
        return (False,0)

# -------------------------------------------------------------------
# ---- is a number (int, float, scientific notation)
# -------------------------------------------------------------------

def is_a_number(s):

    x,n = is_int(s)
    if x:
        return True

    x,n = is_float(s)
    if x:
        return True

    return False

# -------------------------------------------------------------------
# ---- main
# -------------------------------------------------------------------

if __name__ == '__main__':

    if not running_python3():
        print()
        print('Must run Python3 - exit program')
        print()
        sys.exit()

    while True:                # loop

        clear_screen()
        print()
        s = get_user_input('Enter data: ')
        if not s:              # empty string?
            break

        (x,n) = is_int(s)
        if x:
            print()
            print(f'You entered the integer {n}')
            pause()
            continue

        (x,n) = is_float(s)
        if x:
            print()
            print(f'You entered the float {n}')
            pause()
            continue

        print()
        print(f'You entered the string "{s}"')
        pause()

    print()
