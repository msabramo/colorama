
from unittest import TestCase, main
from ctypes import windll

from mock import patch

from ..winterm import Color, HANDLE, Intensity, WinTerm

class WinTermTest(TestCase):

    def testInit(self):
        term = WinTerm()
        self.assertEquals(term._fore, Color.GREY)
        self.assertEquals(term._back, Color.BLACK) 
        self.assertEquals(term._intensity, Intensity.NORMAL) 

    def DONTtestDefaults(self):
        self.fail('default fore and back should read from terminal current')
        self.fail('resetall untested')

    def testCombinedAttrs(self):
        term = WinTerm()

        term._fore = 0
        term._back = 0
        term._intensity = 0
        self.assertEquals(term.combined_attrs, 0)

        term._fore = Color.YELLOW
        self.assertEquals(term.combined_attrs, Color.YELLOW)

        term._back = Color.MAGENTA
        self.assertEquals(
            term.combined_attrs,
            Color.YELLOW + Color.MAGENTA * 16)

        term._intensity = Intensity.BRIGHT
        self.assertEquals(
            term.combined_attrs,
            Color.YELLOW + Color.MAGENTA * 16 + Intensity.BRIGHT)

    @patch('colorama.winterm.windll.kernel32')
    def testFore(self, kernel32):
        term = WinTerm()
        term._fore = 0
        term.fore(5)
        self.assertEquals(term._fore, 5)
        self.assertEquals(
            kernel32.SetConsoleTextAttribute.call_args,
            ((HANDLE, term.combined_attrs), {})
        )


if __name__ == '__main__':
    main()

