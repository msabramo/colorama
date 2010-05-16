http://pypi.python.org/pypi/colorama (docs and download)
http://code.google.com/p/colorama/ (development)

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

None, other than Python. Tested on Python 2.5.5, 2.6.5 & 3.1.2.


Usage
=====

Initialisation
--------------

Applications should initialise Colorama using::

    from colorama import init
    init()

If you are on Windows, the call to ``init()`` will start filtering ANSI escape
sequences out of any text sent to stdout or stderr, and will replace them with
equivalent Win32 calls.

Calling ``init()`` has no effect on other platforms (unless you request other
optional functionality, see keyword args below.) The intention is that
applications can call ``init()`` unconditionally on all platforms, after which
ANSI output should just work.


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


Init Keyword Args
-----------------

``init()`` accepts some kwargs to override default behaviour.

init(autoreset=False):
    If you find yourself repeatedly sending reset sequences to turn off color
    changes at the end of every print, then ``init(autoreset=True)`` will
    automate that::

        from colorama import init
        init(autoreset=True)
        print Fore.RED + 'some red text'
        print 'automatically back to default color again'

init(strip=None):
    Pass ``True`` or ``False`` to override whether ansi codes should be
    stripped from the output. The default behaviour is to strip if on Windows.

init(convert=None):
    Pass ``True`` or ``False`` to override whether to convert ansi codes in the
    output into win32 calls. The default behaviour is to convert if on Windows
    and output is to a tty (terminal).

init(wrap=True):
    On Windows, colorama works by replacing ``sys.stdout`` and ``sys.stderr``
    with proxy objects, which override the .write() method to do their work. If
    this wrapping causes you problems, then this can be disabled by passing
    ``init(wrap=False)``. The default behaviour is to wrap if autoreset or
    strip or convert are True.

    When wrapping is disabled, colored printing on non-Windows platforms will
    continue to work as normal. To do cross-platform colored output, you can
    use Colorama's ``AnsiToWin32`` proxy directly:

        from colorama import init, AnsiToWin32
        init(wrap=False)
        stream = AnsiToWin32(sys.stderr).stream
        print >>stream, Fore.BLUE + 'blue text on stderr'    


Status & Known Problems
=======================

Feature complete as far as colored text goes, but still finding bugs and
occasionally making small changes to the API. I'd like to also handle ANSI
codes which position the text cursor and clear the terminal.

Only tested on WinXP (CMD, Console2) and Ubuntu (gnome-terminal, xterm). Much
obliged if anyone can let me know how it fares elsewhere, in particular on
Macs.

See outstanding issues and wishlist at:
http://code.google.com/p/colorama/issues/list


Development
===========

Tests require Michael Foord's modules 'unittest2' and 'mock', running tests
using::

    unit2 discover -p '*_test.py'

If using 'nosetests' for test discovery, be aware that it applies a proxy of
its own to stdout, which confuses the unit tests. Use 'nosetests -s' to fix
this.


Changes
=======

0.1.9
    Fix incompatibility with Python 2.5 and earlier
    Remove setup.py dependency on setuptools, now uses stdlib distutils
0.1.8
    Fix ghastly errors all over the place on Ubuntu.
    Add init kwargs 'convert' and 'strip', which supercede the old 'wrap'.
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

