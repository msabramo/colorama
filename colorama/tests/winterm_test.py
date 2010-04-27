
from unittest2 import TestCase, main

from mock import Mock, patch

from ..winterm import WinColor, WinStyle, WinTerm


class WinTermTest(TestCase):

    def testInit(self):
        term = WinTerm()
        self.assertEquals(term._fore, WinColor.GREY)
        self.assertEquals(term._back, WinColor.BLACK) 
        self.assertEquals(term._style, WinStyle.NORMAL) 

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

    def testResetAll(self):
        term = WinTerm()
        term.set_console = Mock()
        term._fore = -1
        term._back = -1
        term._style = -1

        term.reset_all()

        self.assertEquals(term._fore, WinColor.GREY)
        self.assertEquals(term._back, WinColor.BLACK)
        self.assertEquals(term._style, WinStyle.NORMAL)
        self.assertEquals(term.set_console.called, True)

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

    @patch('colorama.winterm.windll')
    def testSetConsole(self, mockWindll):
        term = WinTerm()
        term.windll = Mock()
        term.handle = Mock()
        term.set_console()
        self.assertEquals(
            mockWindll.kernel32.SetConsoleTextAttribute.call_args,
            ((term.handle, term.combined_attrs), {})
        )


if __name__ == '__main__':
    main()

