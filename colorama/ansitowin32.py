
import re
import sys

from .ansi import AnsiFore, AnsiBack, AnsiStyle, Style
from .winterm import winterm, WinColor, WinStyle


class AnsiToWin32(object):

    ANSI_RE = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')

    def __init__(self, wrapped, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.enabled = sys.platform.startswith('win')
        self.win32_calls = self.get_win32_calls()
        self.stderr = self.wrapped is sys.stderr

    def get_win32_calls(self):
        if self.enabled and winterm:
            return {
                AnsiStyle.RESET_ALL: (winterm.reset_all, ),
                AnsiStyle.BRIGHT: (winterm.style, WinStyle.BRIGHT),
                AnsiStyle.DIM: (winterm.style, WinStyle.DIM),
                AnsiStyle.NORMAL: (winterm.style, WinStyle.NORMAL),
                AnsiFore.BLACK: (winterm.fore, WinColor.BLACK),
                AnsiFore.RED: (winterm.fore, WinColor.RED),
                AnsiFore.GREEN: (winterm.fore, WinColor.GREEN),
                AnsiFore.YELLOW: (winterm.fore, WinColor.YELLOW),
                AnsiFore.BLUE: (winterm.fore, WinColor.BLUE),
                AnsiFore.MAGENTA: (winterm.fore, WinColor.MAGENTA),
                AnsiFore.CYAN: (winterm.fore, WinColor.CYAN),
                AnsiFore.WHITE: (winterm.fore, WinColor.GREY),
                AnsiFore.RESET: (winterm.fore, ),
                AnsiBack.BLACK: (winterm.back, WinColor.BLACK),
                AnsiBack.RED: (winterm.back, WinColor.RED),
                AnsiBack.GREEN: (winterm.back, WinColor.GREEN),
                AnsiBack.YELLOW: (winterm.back, WinColor.YELLOW),
                AnsiBack.BLUE: (winterm.back, WinColor.BLUE),
                AnsiBack.MAGENTA: (winterm.back, WinColor.MAGENTA),
                AnsiBack.CYAN: (winterm.back, WinColor.CYAN),
                AnsiBack.WHITE: (winterm.back, WinColor.GREY),
                AnsiBack.RESET: (winterm.back, ),
            }
        else:
            return {}


    def __getattr__(self, name):
        return getattr(self.wrapped, name)


    def reset_all(self):
        if self.enabled:
            self.call_win32('m', [0])
        else:
            self.wrapped.write(Style.RESET_ALL)


    def write(self, text):
        if self.enabled:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
        if self.autoreset:
            self.reset_all()


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
        if params == []:
            params = [0]
        if command == 'm':
            for param in params:
                if param in self.win32_calls:
                    func_args = self.win32_calls[param]
                    func = func_args[0]
                    args = func_args[1:]
                    func(*args, stderr=self.stderr)

