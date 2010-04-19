
from unittest2 import TestCase, main

from mock import patch, Mock

from ..winterm import WinColor, HANDLE, WinStyle, WinTerm

class WinTermTest(TestCase):

    def testInit(self):
        term = WinTerm()
        self.assertEquals(term._fore, WinColor.GREY)
        self.assertEquals(term._back, WinColor.BLACK) 
        self.assertEquals(term._style, WinStyle.NORMAL) 

    def DONTtestDefaults(self):
        self.fail('default fore and back should read from terminal current')
        self.fail('resetall untested')


    def testCombinedAttrs(self):
        term = WinTerm()

        term._fore = 0
        term._back = 0
        term._style = 0
        self.assertEquals(term.combined_attrs, 0)

        term._fore = WinColor.YELLOW
        self.assertEquals(term.combined_attrs, WinColor.YELLOW)

        term._back = WinColor.MAGENTA
        self.assertEquals(
            term.combined_attrs,
            WinColor.YELLOW + WinColor.MAGENTA * 16)

        term._style = WinStyle.BRIGHT
        self.assertEquals(
            term.combined_attrs,
            WinColor.YELLOW + WinColor.MAGENTA * 16 + WinStyle.BRIGHT)

    def testFore(self):
        term = WinTerm()
        term.set_console = Mock()
        term._fore = 0

        term.fore(5)

        self.assertEquals(term._fore, 5)
        self.assertEquals(term.set_console.called, True)
    

    def testBack(self):
        term = WinTerm()
        term.set_console = Mock()
        term._back = 0

        term.back(5)

        self.assertEquals(term._back, 5)
        self.assertEquals(term.set_console.called, True)

        
    def testStyle(self):
        term = WinTerm()
        term.set_console = Mock()
        term._style = 0

        term.style(22)

        self.assertEquals(term._style, 22)
        self.assertEquals(term.set_console.called, True)


    @patch('colorama.winterm.windll.kernel32')
    def test_set_console(self, kernel32):
        term = WinTerm()
        term.set_console()
        self.assertEquals(
            kernel32.SetConsoleTextAttribute.call_args,
            ((HANDLE, term.combined_attrs), {})
        )


if __name__ == '__main__':
    main()

