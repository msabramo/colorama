http://code.google.com/p/colorama/

Description
===========

Makes ANSI escape character sequences for producing colored terminal text work
under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text on Unix and Macs. Colorama makes this work on Windows, too. It also
provides some shortcuts to help generate ANSI sequences, and works fine in
conjunction with any other ANSI sequence generation library, such as Termcolor
(http://pypi.python.org/pypi/termcolor.)

This has the upshot of providing a simple cross-platform API for printing
colored terminal text from Python, and has the happy side-effect that existing
applications or libraries which use ANSI sequences to produce colored output on
Linux or Macs can now also work on Windows, simply by calling
``colorama.init()``.

Dependencies
============

None, other than Python. Tested on Python 2.6.5 & 3.1.2.


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
such as Termcolor::

    from colorama import init
    from termcolor import colored

    # use Colorama to make Termcolor work on Windows too
    init()

    # then use Termcolor for all colored text output
    print colored('Hello, World!', 'green', 'on_red')

Available formatting constants are::

    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, DEFAULT.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, DEFAULT.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL

Style.RESET_ALL resets foreground, background and brightness. Colorama will
perform this reset automatically on program exit.

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


Status & Known Problems
=======================

Just became feature complete. Consider it alpha.

Only tested on WinXP (CMD, Console2) and Ubuntu (gnome-terminal, xterm). Much
obliged if anyone can let me know how it fares elsewhere, in particular on
Macs.

See outstanding bugs, refactoring and wishlist in TODO.txt.
(http://code.google.com/p/colorama/source/browse/TODO.txt)

Some differences between Windows and other terminals exist, which Colorama
currently makes no attempt to meddle with:

On Linux terminals, scrolling fills the whole new line with the current
background color. On Windows, the new line is filled with the default
background color.

On Linux, the foreground color has dim / normal / bright settings, but
the background is constant. On Windows, both foreground and background
have independent normal / bright settings. Colorama maps 'bright' ANSI codes to
use a bright background color on Windows, to emulate the missing third level of
brightness. This might cause unexpected uglyness for particular existing
applications. See screenshots at http://tartley.com/?p=1062.

On Linux terminals, the 'RESET' background and foreground colors are
potentially distinct from all other colors. On Windows, Back.RESET and
Fore.RESET produce an RGB which is indistinguishable from one of the other
color entries.

Only the colors and dim/bright subset of ANSI 'm' commands are recognised.
There are many other ANSI sequences (eg. moving cursor position.) These are
currently silently stripped from the output on Windows.



Development
===========

Tests require Michael Foord's modules 'unittest2' and 'mock', running tests
using::

    unit2 discover -p '*_test.py'

Colorama does not play nice with nosetests. Nose captures stdout by wrapping
it in a StringIO, which confuses colorama's unit tests' expectations about the
identity of stdout.


Changes
=======

0.1.7
    Python 3 compatible.
    Fix: Now strips ansi on windows without necessarily converting it to
    win32 calls (eg. if output is not a tty.)
    Fix: Flaky interaction of interleaved ansi sent to stdout and stderr.
    Improved demo.sh (hg checkout only.)
0.1.6
    Fix ansi sequences with no params now default to parmlist of [0]
    Fix flaky behaviour of autoreset and reset_all atexit.
    Fix stacking of repeated atexit calls - now just called once.
    Fix ghastly import problems while running tests.
    demo.py (hg checkout only) now demonstrates autoreset and reset atexit.
    provide colorama.__version__, used by setup.py
    Tests defanged so they no longer actually change terminal color when run.
0.1.5
    Now works on Ubuntu.
0.1.4
    Implemented RESET_ALL on application exit
0.1.3
    Implemented init(wrap=False)
0.1.2
    Implemented init(autoreset=True)
0.1.1
    Minor tidy
0.1
    Works on Windows for foreground color, background color, bright or dim

