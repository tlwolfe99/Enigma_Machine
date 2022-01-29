#!/usr/bin/python3
# ===================================================================
#
# ===================================================================

from EnigmaConfig import EnigmaConfig
import os
import sys

# ---- configuration file name on the command line?

configfile = 'enigma_config.csv'

if len(sys.argv) > 1:
    configfile = sys.argv[1]

if not os.path.exists(configfile):
    print()
    print(f'Can not find enigma configuration file ({configfile})')
    print()
    sys.exit()

# ---- get configuration

config = EnigmaConfig('enigma_config.csv')

# ---- display configuration

config.display_stats()
