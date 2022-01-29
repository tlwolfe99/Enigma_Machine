#!/usr/bin/python3
# ===================================================================
# Test command line arguments
# ===================================================================

import sys

# ---- remove first argument

print()
print(f'before: {sys.argv}')
sys.argv.pop(0)
print(f'after : {sys.argv}')

# ---- print remaining argument list

print()
for i in range(len(sys.argv)):
    print(f'[{i}]  {sys.argv[i]}')
print()

# ---- print remaining argument list length

print(f'argument length is {len(sys.argv)}')

