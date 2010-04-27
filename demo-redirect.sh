#!/usr/bin/env bash

python 2>out <<EOF
import sys
from colorama import init, Fore

init()

print >>sys.stdout, Fore.RED + 'Red stdout, ',
print >>sys.stderr, Fore.BLUE + 'Blue stderr,',
print >>sys.stdout, 'Further stdout should be red'
EOF

