#!/usr/bin/env bash

python 2>err <<EOF
import sys
from colorama import init, Fore

init()

print Fore.RED + 'Red stdout.',
print >>sys.stderr, Fore.BLUE + 'ANSI stripped from blue stderr.'
print 'Further stdout should be red'
EOF

echo 'and the redirected stderr:'
cat err

rm -rf err out

