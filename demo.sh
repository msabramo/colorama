#!/usr/bin/env bash

# Script to demonstrate features of colorama

# This demo, which can manually be visually verified, exists because we don't
# have an automated system test.

# Implemented as a bash script which invokes python so that we can test the
# behaviour on exit, which resets default colors again.

python 2>err <<EOF
import sys

from colorama import init, Fore, Back, Style

init()

# example of common usage
print Fore.GREEN + 'green' + Fore.RED + 'red' + Fore.RESET + 'normal',
print Back.GREEN + 'green' + Back.RED + 'red' + Back.RESET + 'normal',
print Style.DIM + 'dim' + \
    Style.NORMAL + 'normal' + \
    Style.BRIGHT + 'bright'
print Style.RESET_ALL

FORES = [
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
]
BACKS = [
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

# print grid of all colors and brightnesses
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

    print Style.RESET_ALL

# check autoreset works
init(autoreset=True)
print
print Fore.CYAN + Back.MAGENTA + Style.BRIGHT + 'colored', 'autoreset'

# check reset_all is called at exit
init(autoreset=False)
print Fore.YELLOW + Back.BLUE + Style.BRIGHT + 'colored',

EOF

echo 'reset at exit'

python 2>err <<EOF2
import sys
from colorama import init, Fore

init()

# check that ANSI in redirected stderr is stripped
print Fore.RED + 'Red stdout.',
print >>sys.stderr, Fore.BLUE + 'ANSI stripped from blue redirected stderr.'

# check that stripped ANSI in redirected stderr did not affect stdout
print 'Further stdout should be red'
EOF2

cat err

rm -rf err out


