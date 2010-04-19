#! /usr/bin/env python

import sys

from colorama import init, Fore, Back, Style

init()

print Fore.GREEN + 'green' + Fore.RED + 'red' + Fore.RESET + 'normal'
print Back.GREEN + 'green' + Back.RED + 'red' + Back.RESET + 'normal'
print Style.DIM + 'dim',
print Style.NORMAL + 'normal',
print Style.BRIGHT + 'bright'
print Style.NORMAL

FORES = [
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
    Fore.RESET,
]
BACKS = [
    Back.RESET,
    Back.BLACK,
    Back.RED,
    Back.GREEN,
    Back.YELLOW,
    Back.BLUE,
    Back.MAGENTA,
    Back.CYAN,
    Back.WHITE,
]
STYLES = [
    Style.DIM,
    Style.NORMAL,
    Style.BRIGHT,
]

# use stdout.write to write chars with no newline nor spaces between them
for background in BACKS:
    sys.stdout.write(background)

    for inten in STYLES:
        sys.stdout.write(inten)

        for foreground in FORES:
            sys.stdout.write(foreground)

            sys.stdout.write('XX')

        sys.stdout.write(' ')

    print Style.RESET_ALL

