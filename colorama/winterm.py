
from ctypes import windll


# from wincon.h
class WinColor(object):
    BLACK   = 0
    BLUE    = 1
    GREEN   = 2
    CYAN    = 3
    RED     = 4
    MAGENTA = 5
    YELLOW  = 6
    GREY    = 7

# from wincon.h
class WinStyle(object):
    DIM    = 0x00
    NORMAL = 0x08
    BRIGHT = 0x88

# from winbase.h
STD_OUTPUT_HANDLE= -11
HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


class WinTerm(object):

    def __init__(self):
        self.reset_all()

    @property
    def combined_attrs(self):
        return self._fore + self._back * 16 + self._style

    def reset_all(self):
        self._fore = WinColor.GREY
        self._back = WinColor.BLACK
        self._style = WinStyle.NORMAL
        self.set_console()

    def fore(self, fore=None):
        if fore is None:
            fore = WinColor.GREY
        self._fore = fore
        self.set_console()

    def back(self, back=None):
        if back is None:
            back = WinColor.BLACK
        self._back = back
        self.set_console()

    def style(self, style=None):
        self._style = style
        self.set_console()

    def set_console(self):
        windll.kernel32.SetConsoleTextAttribute(HANDLE, self.combined_attrs)

