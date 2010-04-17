
import sys

from colorama.colorama import wrap, Ansi

fores = [
    Ansi.BLACK,
    Ansi.RED,
    Ansi.GREEN,
    Ansi.YELLOW,
    Ansi.BLUE,
    Ansi.MAGENTA,
    Ansi.CYAN,
    Ansi.WHITE,
]

backs = [
    Ansi.BLACK_BG,
    Ansi.RED_BG,
    Ansi.GREEN_BG,
    Ansi.YELLOW_BG,
    Ansi.BLUE_BG,
    Ansi.MAGENTA_BG,
    Ansi.CYAN_BG,
    Ansi.WHITE_BG,
]

styles = [
    Ansi.DIM,
    Ansi.NORMAL,
    Ansi.BRIGHT,
#    Ansi.UNDERLINE,
#    Ansi.BLINK,
#    Ansi.REVERSE,
#    Ansi.CONCEALED,
]


sys.stdout = wrap(sys.stdout)
# term = ColorStream(sys.stdout)
print 'go' + Ansi.RED + 'stop' + Ansi.DEFAULT + 'normal'
print 'go' + Ansi.RED_BG + 'stop' + Ansi.DEFAULT_BG + 'normal'

for st in styles:
    for bg in backs:
        for fg in fores:
            sys.stdout.write(fg + bg + st + 'X')
    print

print Ansi.WHITE + Ansi.BLACK_BG + Ansi.NORMAL

