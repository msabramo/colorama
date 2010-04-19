#! /usr/bin/env python

import sys

from colorama import init, Fore, Back, Style

init()

print Fore.GREEN + 'green' + Fore.RED + 'red' + Fore.RESET + 'normal'
print Back.GREEN + 'green' + Back.RED + 'red' + Back.RESET + 'normal'
print Style.DIM+ 'dim' + Style.NORMAL + 'normal' + Style.BRIGHT + 'bright'
print Style.NORMAL

for st in Style.ALL:
    for bg in Back.ALL:
        for fg in Fore.ALL:
            # use stdout.write to write X chars with no space between them
            sys.stdout.write(fg + bg + st + 'X')
    print Style.RESET_ALL

