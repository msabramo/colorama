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
importing and initialising Colorama.


Status
======

In development. Features described in this documentation might not be
implemented yet.


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
'autoreset', see below) The intention is that all applications should call
init() unconditionally, then their colored text output simply works on all
platforms.

Colored Output
--------------

Cross-platform printing of colored text can then be done::

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

Available formatting constants are:

    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, ALL, DEFAULT.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, ALL, DEFAULT.
    Style: DIM, DEFAULT, BRIGHT, ALL, RESET_ALL

Style.RESET_ALL resets all attributes: foreground, background and brightness.
Colorama will perform this reset automatically on program exit.

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
write() to do their work. Using init(autoreset=True) will do this wrapping
on all platforms, not just Windows.

If these proxy objects wrapping stdout and stderr cause you problems, then this
can be disabled using init(wrap=False), and you can instead access Colorama's
AnsiToWin32 proxy directly. Any attribute access on this object will be
forwarded to the stream it wraps, apart from .write(), which on Windows is
overridden to first perform the ANSI to Win32 conversion on text::

    from colorama import init, AnsiToWin32
    init(wrap=False)

    stream = AnsiToWin32(sys.stderr)
    print >>stream, Fore.BLUE + 'blue text on stderr'    

Development
===========

Tests require Michael Foord's Mock module. I have been using nose to run the
tests although they may work without it.

Known Problems
==============

Only stdout is currently implimented: stderr is not affected.

Only recognised ANSI escape sequences (ie colors, dim/bright) are filtered out
of the output text. Unrecognised sequences (eg. moving the text cursor) appear
as gobbledygook in the output on Windows. Ideally, these could be implimented
using win32 calls too. In the meantime, is it better to filter them out of the
output?

