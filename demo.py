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

NAMES = {
    Fore.BLACK: 'black',
    Fore.RED: 'red',
    Fore.GREEN: 'green',
    Fore.YELLOW: 'yellow',
    Fore.BLUE: 'blue',
    Fore.MAGENTA: 'magenta',
    Fore.CYAN: 'cyan',
    Fore.WHITE: 'white',
    Fore.RESET: 'reset',
    Back.BLACK: 'black',
    Back.RED: 'red',
    Back.GREEN: 'green',
    Back.YELLOW: 'yellow',
    Back.BLUE: 'blue',
    Back.MAGENTA: 'magenta',
    Back.CYAN: 'cyan',
    Back.WHITE: 'white',
    Back.RESET: 'reset',
}

# use stdout.write to write chars with no newline nor spaces between them
sys.stdout.write('        ')
for foreground in FORES:
    sys.stdout.write('%s%-7s' % (foreground, NAMES[foreground]))
print

for background in BACKS:
    sys.stdout.write('%s%-7s%s %s' %
       (background, NAMES[background], Back.RESET, background))

    for foreground in FORES:
        sys.stdout.write(foreground)

        for brightness in STYLES:
            sys.stdout.write(brightness)

            sys.stdout.write('X ')

        sys.stdout.write(Style.RESET_ALL + ' ' + background)

    print

print Style.RESET_ALL

