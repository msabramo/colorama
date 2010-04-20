http://code.google.com/p/colorama/

Description
===========

Provides a simple cross-platform API to print colored terminal text from Python
applications.

ANSI escape character sequences are commonly used to produce colored terminal
text on Macs and Unix. Colorama provides some shortcuts to generate these
sequences, and makes them work on Windows too.

This has the happy side-effect that existing applications or libraries which
already use ANSI sequences to produce colored output on Linux or Macs (eg.
using packages like 'termcolor') can now also work on Windows, simply by
calling ``colorama.init()``.

Status: Feature complete. Alpha release.


Dependencies
============

None, other than Python. Tested on Python 2.6.5.


Usage
=====

Initialisation
--------------

Applications should initialise Colorama using::

    from colorama import init
    init()

If you are on Windows, the call to ''init()'' will start filtering ANSI escape
sequences out of any text sent to stdout or stderr, and will replace them with
equivalent Win32 calls.

Calling ''init()'' has no effect on other platforms (unless you use
'autoreset', see below) The intention is that applications should call init()
unconditionally to make subsequent ANSI output just work on all platforms.

Colored Output
--------------

Cross-platform printing of colored text can then be done using Colorama's
constant shorthand for ANSI escape sequences::

    from colorama import Fore, Back, Style
    print Fore.RED + 'some red text'
    print Back.GREEN + and with a green background'
    print Style.DIM + 'and in dim text'
    print + Fore.DEFAULT + Back.DEFAULT + Style.DEFAULT
    print 'back to normal now'

or simply by manually printing ANSI sequences from your own code::

    print '/033[31m' + 'some red text'
    print '/033[30m' # and reset to default color

or Colorama can be used happily in conjunction with existing ANSI libraries
such as Termcolor (http://pypi.python.org/pypi/termcolor)::

    # use Colorama to make Termcolor work on Windows too
    from colorama import init
    init()

    # then use Termcolor for all colored text output
    from termcolor import colored
    print colored('Hello, World!', 'green', 'on_red')

Available formatting constants are::

    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, DEFAULT.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, DEFAULT.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL

Style.RESET_ALL resets foreground, background and brightness.
Colorama will perform this reset automatically on program exit *(Not
implemented)*.

Autoreset
---------

If you find yourself repeatedly sending reset sequences to turn off color
changes at the end of every print, then init(autoreset=True) will automate
that::

    from colorama import init
    init(autoreset=True)
    print Fore.RED + 'some red text'
    print 'automatically back to default color again'

Without wrapping stdout
-----------------------

Colorama works by wrapping stdout and stderr with proxy objects, that override
write() to do their work. Using autoreset (above) will do this wrapping on all
platforms, not just Windows.

If these proxy objects wrapping stdout and stderr cause you problems, then this
can be disabled using init(wrap=False). You can then access Colorama's
AnsiToWin32 proxy directly. Any attribute access on this object will be
forwarded to the stream it wraps, apart from .write(), which on Windows is
overridden to first perform the ANSI to Win32 conversion on text::

    from colorama import init, AnsiToWin32
    init(wrap=False)

    stream = AnsiToWin32(sys.stderr)
    print >>stream, Fore.BLUE + 'blue text on stderr'    

Development
===========

Tests require Michael Foord's modules 'unittest2' and 'mock'. I have been using
nose's 'nosetests' to run the tests although they may run without it, using::

    python -m colorama.tests.<module>

Changes
=======

0.1.4
    Implemented RESET_ALL on application exit
0.1.3
    Implemented init(wrap=False)
0.1.2
    Implemented init(autoreset=True)
0.1.1
    Minor tidy
0.1
    Works for foreground color, background color, bright or dim

Known Problems
==============

Only the colors and dim/bright subset of ANSI 'm' commands are recognised.
There are many other ANSI sequences (eg. moving cursor position) that could
also be usefully converted into win32 calls. These are currently silently
stripped from the output on Windows.

