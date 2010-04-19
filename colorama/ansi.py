'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''

CSI = '\033['


class AnsiCodes(object):

    def __init__(self, codes):
        for name in dir(codes):
            if not name.startswith('_'):
                value = getattr(codes, name)
                setattr(self, name, self.code_to_chars(value))

    def code_to_chars(self, code):
        return CSI + str(code) + 'm'


class AnsiStyle:
    RESET_ALL = 0
    BRIGHT    = 1
    DIM       = 2
    NORMAL    = 22

class AnsiFore:
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37
    RESET   = 39

class AnsiBack:
    BLACK   = 40
    RED     = 41
    GREEN   = 42
    YELLOW  = 43
    BLUE    = 44
    MAGENTA = 45
    CYAN    = 46
    WHITE   = 47
    RESET   = 49
    

Fore = AnsiCodes( AnsiFore )
Fore.ALL = [
    Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
    Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
]

Back = AnsiCodes( AnsiBack )
Back.ALL = [
    Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
    Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE,
]

Style = AnsiCodes( AnsiStyle )
Style.ALL = [
    Style.DIM, Style.NORMAL, Style.BRIGHT,
]

