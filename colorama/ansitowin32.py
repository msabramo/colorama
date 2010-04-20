
import re
import sys

from .ansi import AnsiFore, AnsiBack, AnsiStyle
from .winterm import WinColor, WinStyle, WinTerm


winterm = WinTerm()

win32_calls = {
    AnsiStyle.RESET_ALL: winterm.reset_all,
    AnsiStyle.BRIGHT: lambda: winterm.style(WinStyle.BRIGHT),
    AnsiStyle.DIM: lambda: winterm.style(WinStyle.DIM),
    AnsiStyle.NORMAL: lambda: winterm.style(WinStyle.NORMAL),
    AnsiFore.BLACK: lambda: winterm.fore(WinColor.BLACK),
    AnsiFore.RED: lambda: winterm.fore(WinColor.RED),
    AnsiFore.GREEN: lambda: winterm.fore(WinColor.GREEN),
    AnsiFore.YELLOW: lambda: winterm.fore(WinColor.YELLOW),
    AnsiFore.BLUE: lambda: winterm.fore(WinColor.BLUE),
    AnsiFore.MAGENTA: lambda: winterm.fore(WinColor.MAGENTA),
    AnsiFore.CYAN: lambda: winterm.fore(WinColor.CYAN),
    AnsiFore.WHITE: lambda: winterm.fore(WinColor.GREY),
    AnsiFore.RESET: lambda: winterm.fore(),
    AnsiBack.BLACK: lambda: winterm.back(WinColor.BLACK),
    AnsiBack.RED: lambda: winterm.back(WinColor.RED),
    AnsiBack.GREEN: lambda: winterm.back(WinColor.GREEN),
    AnsiBack.YELLOW: lambda: winterm.back(WinColor.YELLOW),
    AnsiBack.BLUE: lambda: winterm.back(WinColor.BLUE),
    AnsiBack.MAGENTA: lambda: winterm.back(WinColor.MAGENTA),
    AnsiBack.CYAN: lambda: winterm.back(WinColor.CYAN),
    AnsiBack.WHITE: lambda: winterm.back(WinColor.GREY),
    AnsiBack.RESET: lambda: winterm.back(),
}


class AnsiToWin32(object):

    ANSI_RE = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')

    def __init__(self, wrapped, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.enabled = sys.platform.startswith('win')
        self.winterm = winterm


    def __getattr__(self, name):
        return getattr(self.wrapped, name)


    def write(self, text):
        if self.enabled:
            self.write_and_convert(text)
            if self.autoreset:
                self.winterm.reset_all()
        else:
            self.wrapped.write(text)

    def write_and_convert(self, text):
        cursor = 0
        for match in self.ANSI_RE.finditer(text):
            start, end = match.span()
            self.write_snippet(text, cursor, start)

            paramstring, command = match.groups()
            params = self.extract_params(paramstring)
            self.call_win32(command, params)

            cursor = end

        self.write_snippet(text, cursor, len(text))


    def write_snippet(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])


    def extract_params(self, paramstring):
        def split(paramstring):
            for p in paramstring.split(';'):
                if p != '':
                    yield int(p)
        return tuple(split(paramstring))


    def call_win32(self, command, params):
        if command == 'm':
            for param in params:
                if param in win32_calls:
                    win32_calls[param]()

