#! /usr/bin/env python

import sys

from colorama import init, Fore, Back, Intensity, RESET_ALL

init()

print Fore.GREEN + 'green' + Fore.RED + 'red' + Fore.RESET + 'normal'
print Back.GREEN + 'green' + Back.RED + 'red' + Back.RESET + 'normal'
print Intensity.DIM+ 'dim' + Intensity.NORMAL + 'normal' + Intensity.BRIGHT + 'bright'
print Intensity.NORMAL

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
INTENSITIES = [
    Intensity.DIM,
    Intensity.NORMAL,
    Intensity.BRIGHT,
]

# use stdout.write to write chars with no newline nor spaces between them
for background in BACKS:
    sys.stdout.write(background)
    for foreground in FORES:
        sys.stdout.write(foreground)
        for inten in INTENSITIES:
            sys.stdout.write(inten)

            sys.stdout.write('X')

    print RESET_ALL

