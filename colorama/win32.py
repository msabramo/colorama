# Copyright (c) 2010 Jonathan Hartley <tartley@tartley.com>
# See LICENSE.txt

try:
    from ctypes import windll
except ImportError:
    windll = None
    STDOUT_HANDLE = None
    STDERR_HANDLE = None
else:
    from ctypes import (
        byref, Structure, c_char, c_short, c_uint32, c_ushort
    )

    # constants from winbase.h
    STDOUT_HANDLE = windll.kernel32.GetStdHandle(-11)
    STDERR_HANDLE = windll.kernel32.GetStdHandle(-12)

SHORT = c_short
WORD = c_ushort
DWORD = c_uint32
TCHAR = c_char

class COORD(Structure):
    """struct in wincon.h"""
    _fields_ = [
        ('X', SHORT),
        ('Y', SHORT),
    ]

class  SMALL_RECT(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT),
    ]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
    ]

def GetConsoleScreenBufferInfo(handle):
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    success = windll.kernel32.GetConsoleScreenBufferInfo(handle, byref(csbi))
    assert success
    return csbi

def SetConsoleTextAttribute(handle, attrs):
    success = windll.kernel32.SetConsoleTextAttribute(handle, attrs)
    assert success

def SetConsoleCursorPosition(handle, position):
    position = COORD(*position)
    success = windll.kernel32.SetConsoleCursorPosition(handle, position)
    assert success

def FillConsoleOutputCharacter(handle, char, length, start):
    char = TCHAR(char)
    length = DWORD(length)
    start = COORD(*start)
    num_written = DWORD(0)
    # AttributeError: function 'FillConsoleOutputCharacter' not found
    # could it just be that my types are wrong?
    success = windll.kernel32.FillConsoleOutputCharacter(
        handle, char, length, start, byref(num_written))
    assert success
    return num_written.value


if __name__=='__main__':
    # SetConsoleTextAttribute(STDOUT_HANDLE, 7)
    #FillConsoleOutputCharacter(STDOUT_HANDLE, '.', 81, (1, 2))
    # SetConsoleCursorPosition(STDOUT_HANDLE, (1, 2))
    print GetConsoleScreenBufferInfo(STDOUT_HANDLE)

