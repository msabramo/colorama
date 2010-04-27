
windll = None
try:
    from ctypes import windll
except ImportError:
    pass


# from winbase.h
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE= -12

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


class WinTerm(object):

    def __init__(self):
        self.default_attrs()
        if windll:
            self.out_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            self.err_handle = windll.kernel32.GetStdHandle(STD_ERROR_HANDLE)

    @property
    def combined_attrs(self):
        return self._fore + self._back * 16 + self._style

    def default_attrs(self):
        self._fore = WinColor.GREY
        self._back = WinColor.BLACK
        self._style = WinStyle.NORMAL

    def reset_all(self, on_stderr=None):
        self.default_attrs()
        self.set_console()

    def fore(self, fore=None, on_stderr=False):
        if fore is None:
            fore = WinColor.GREY
        self._fore = fore
        self.set_console(on_stderr=on_stderr)

    def back(self, back=None, on_stderr=False):
        if back is None:
            back = WinColor.BLACK
        self._back = back
        self.set_console(on_stderr=on_stderr)

    def style(self, style=None, on_stderr=False):
        self._style = style
        self.set_console(on_stderr=on_stderr)

    def set_console(self, on_stderr=False):
        if windll:
            handle = self.err_handle if on_stderr else self.out_handle
            windll.kernel32.SetConsoleTextAttribute(handle, self.combined_attrs)


winterm = WinTerm()

