
from contextlib import contextmanager
import sys
from unittest import TestCase, main

import colorama
from colorama import AnsiToWin32
from colorama.ansitowin32 import winterm

from mock import Mock, patch

@contextmanager
def platform(name):
    orig = sys.platform
    sys.platform = name
    yield
    sys.platform = orig


class AnsiToWin32Test(TestCase):

    def tearDown(self):
        winterm.reset_all()

    def testInit(self):
        mockStdout = object()
        auto = object()
        stream = AnsiToWin32(mockStdout, autoreset=auto)
        self.assertEquals(stream.wrapped, mockStdout)
        self.assertEquals(stream.autoreset, auto)

    def testEnabledOnWindows(self):
        with platform('windows'):
            stream = AnsiToWin32(None)
            self.assertTrue(stream.enabled)

    def testDisabledOffWindows(self):
        with platform('darwin'):
            stream = AnsiToWin32(None)
            self.assertFalse(stream.enabled)

    def testIsAProxy(self):
        mock = Mock()
        atw32 = AnsiToWin32( mock )
        self.assertTrue( atw32.random_attr is mock.random_attr )

    def testWriteConvertsIfEnabled(self):
        mockStdout = Mock()
        stream = AnsiToWin32(mockStdout)
        stream.wrapped = Mock()
        stream.write_and_convert = Mock()
        stream.enabled = True

        stream.write('abc')

        self.assertFalse(stream.wrapped.write.called)
        self.assertEquals(stream.write_and_convert.call_args, (('abc',), {}))

    def testWriteDoesNotConvertIfDisabled(self):
        mockStdout = Mock()
        stream = AnsiToWin32(mockStdout)
        stream.wrapped = Mock()
        stream.write_and_convert = Mock()
        stream.enabled = False

        stream.write('abc')
        
        self.assertFalse(stream.write_and_convert.called)
        self.assertEquals(stream.wrapped.write.call_args, (('abc',), {}))

    def testWriteAutoresetsIfOn(self):
        stream = AnsiToWin32(Mock())
        stream.enabled = True
        stream.write_and_convert = Mock()
        stream.autoreset = True
        stream.winterm = Mock()

        stream.write('abc')
        
        self.assertEqual(
            stream.winterm.method_calls[-1],
            ('reset_all', (), {}) )

    def testWriteDoesntAutoresetIfOff(self):
        stream = AnsiToWin32(Mock())
        stream.enabled = True
        stream.write_and_convert = Mock()
        stream.autoreset = False
        stream.winterm = Mock()

        stream.write('abc')
        
        self.assertEqual(stream.winterm.method_calls, [])

    def testWriteAndConvertWritesPlainText(self):
        stream = AnsiToWin32(Mock())
        stream.write_and_convert( 'abc' )
        self.assertEquals( stream.wrapped.write.call_args, (('abc',), {}) )

    def testWriteAndConvertStripsAllValidAnsi(self):
        stream = AnsiToWin32(Mock())
        data = [
            'abc\033[mdef',
            'abc\033[0mdef',
            'abc\033[2mdef',
            'abc\033[02mdef',
            'abc\033[002mdef',
            'abc\033[40mdef',
            'abc\033[040mdef',
            'abc\033[0;1mdef',
            'abc\033[40;50mdef',
            'abc\033[50;30;40mdef',
            'abc\033[Adef',
            'abc\033[0Gdef',
            'abc\033[1;20;128Hdef',
        ]
        for datum in data:
            stream.wrapped.write.reset_mock()
            stream.write_and_convert( datum )
            self.assertEquals(
               [args[0] for args in stream.wrapped.write.call_args_list],
               [ ('abc',), ('def',) ]
            )

    def testWriteAndConvertSkipsEmptySnippets(self):
        stream = AnsiToWin32(Mock())
        stream.write_and_convert( '\033[40m\033[41m' )
        self.assertFalse( stream.wrapped.write.called )

    def testWriteAndConvertCallsWin32WithParamsAndCommand(self):
        stream = AnsiToWin32(Mock())
        stream.call_win32 = Mock()
        stream.extract_params = Mock(return_value='params')
        data = {
            'abc\033[adef':         ('a', 'params'),
            'abc\033[;;bdef':       ('b', 'params'),
            'abc\033[0cdef':        ('c', 'params'),
            'abc\033[;;0;;Gdef':    ('G', 'params'),
            'abc\033[1;20;128Hdef': ('H', 'params'),
        }
        for datum, expected in data.iteritems():
            stream.call_win32.reset_mock()
            stream.write_and_convert( datum )
            self.assertEquals( stream.call_win32.call_args[0], expected )

    def testExtractParams(self):
        stream = AnsiToWin32(Mock())
        data = {
            '':               (),
            ';;':             (),
            '2':              (2,),
            ';;002;;':        (2,),
            '0;1':            (0, 1),
            ';;003;;456;;':   (3, 456),
            '11;22;33;44;55': (11, 22, 33, 44, 55),
        }
        for datum, expected in data.iteritems():
            self.assertEquals(stream.extract_params(datum), expected)

    @patch('colorama.ansitowin32.win32_calls', {})
    def testCallWin32UsesLookup(self):
        listener = Mock()
        colorama.ansitowin32.win32_calls.clear()
        colorama.ansitowin32.win32_calls.update( {
            1: lambda: listener(11),
            2: lambda: listener(22),
            3: lambda: listener(33),
        } )
        stream = AnsiToWin32(Mock())
        stream.call_win32('m', (3, 1, 99, 2))
        self.assertEquals(
            [a[0][0] for a in listener.call_args_list],
            [33, 11, 22] )


if __name__ == '__main__':
    main()

