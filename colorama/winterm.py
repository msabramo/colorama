
from ctypes import Structure, c_short, c_ushort, byref, windll


# from wincon.h
class Color(object):
    BLACK   = 0
    BLUE    = 1
    GREEN   = 2
    CYAN    = 3
    RED     = 4
    MAGENTA = 5
    YELLOW  = 6
    GREY    = 7

# from wincon.h
class Intensity(object):
    DIM    = 0x00
    NORMAL = 0x08
    BRIGHT = 0x88

# from winbase.h
STD_OUTPUT_HANDLE= -11
HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


class WinTerm(object):

    def __init__(self):
        self._fore = Color.GREY
        self._back = Color.BLACK
        self._intensity = Intensity.NORMAL

    @property
    def combined_attrs(self):
        return self._fore + self._back * 16 + self._intensity

    def fore(self, fore=None):
        if fore is None:
            fore = Color.GREY
        self._fore = fore
        self.set_console()

    def set_console(self):
        windll.kernel32.SetConsoleTextAttribute(HANDLE, self.combined_attrs)

