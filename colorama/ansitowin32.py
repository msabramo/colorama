
import re
import sys

from .ansi import AnsiFore, AnsiBack, AnsiStyle
from .winterm import Color, Intensity, WinTerm


winterm = WinTerm()

win32_calls = {
    # Style.RESET_ALL: winterm.reset_all,
    # Style.BRIGHT: lambda: winterm.intensity(Intensity.BRIGHT),
    # Style.DIM: lambda: winterm.intensity(Intensity.DIM),
    # Style.NORMAL: lambda: winterm.intensity(Intensity.NORMAL),
    AnsiFore.BLACK: lambda: winterm.fore(Color.BLACK),
    AnsiFore.RED: lambda: winterm.fore(Color.RED),
    AnsiFore.GREEN: lambda: winterm.fore(Color.GREEN),
    AnsiFore.YELLOW: lambda: winterm.fore(Color.YELLOW),
    AnsiFore.BLUE: lambda: winterm.fore(Color.BLUE),
    AnsiFore.MAGENTA: lambda: winterm.fore(Color.MAGENTA),
    AnsiFore.CYAN: lambda: winterm.fore(Color.CYAN),
    AnsiFore.WHITE: lambda: winterm.fore(Color.GREY),
    AnsiFore.RESET: lambda: winterm.fore(),
    # Ansi.BLACK: lambda: winterm.back(Color.BLACK),
    # Ansi.RED: lambda: winterm.back(Color.RED),
    # Ansi.GREEN: lambda: winterm.back(Color.GREEN),
    # Ansi.YELLOW: lambda: winterm.back(Color.YELLOW),
    # Ansi.BLUE: lambda: winterm.back(Color.BLUE),
    # Ansi.MAGENTA: lambda: winterm.back(Color.MAGENTA),
    # Ansi.CYAN: lambda: winterm.back(Color.CYAN),
    # Ansi.WHITE: lambda: winterm.back(Color.GREY),
    # Ansi.DEFAULT: lambda: winterm.back(Color.DEFAULT),
}


class AnsiToWin32(object):

    ANSI_RE = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')

    def __init__(self, wrapped, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.enabled = sys.platform.startswith('win')


    def __getattr__(self, name):
        return getattr(self.wrapped, name)


    def write(self, text):
        if self.enabled:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)


    def write_and_convert(self, text):
        cursor = 0
        for match in self.ANSI_RE.finditer(text):
            start, end = match.span()
            self.write_snippet(text, cursor, start)

            self.call_win32(*match.groups())

            cursor = end

        self.write_snippet(text, cursor, len(text))


    def write_snippet(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])


    def call_win32(self, paramstring, command):
        if command == 'm':
            params = self.extract_params(paramstring)
            for param in params:
                if param in win32_calls:
                    win32_calls[param]()
        

    def extract_params(self, params):
        def split(text):
            for p in params.split(';'):
                if p != '':
                    yield int(p)
        return tuple(split(params))

