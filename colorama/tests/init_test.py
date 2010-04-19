
from StringIO import StringIO
import sys
from unittest import TestCase, main

from .. import init, AnsiToWin32

from .utils import platform

stdout_orig = sys.stdout
stderr_orig = sys.stderr

class InitTest(TestCase):

    def setUp(self):
        # sanity check
        self.assertNotWrapped()

    def tearDown(self):
        sys.stdout = stdout_orig
        sys.stderr = stderr_orig

    def assertWrapped(self):
        # note that nosetests also wraps stdout (a file) with some proxy, so
        # assertions on identity are tricky. Just assert by type instead.
        self.assertEqual(type(sys.stdout), AnsiToWin32)
        self.assertNotEqual(type(sys.stdout.wrapped), AnsiToWin32)

        self.assertEqual(type(sys.stderr), AnsiToWin32)
        self.assertNotEqual(type(sys.stderr.wrapped), AnsiToWin32)

    def assertNotWrapped(self):
        self.assertNotEqual(type(sys.stdout), AnsiToWin32)
        self.assertNotEqual(type(sys.stderr), AnsiToWin32)

    def testInitWrapsOnWindows(self):
        with platform('windows'):
            init()
            self.assertWrapped()

    def testInitDoesntWrapOnNonWindows(self):
        with platform('darwin'):
            init()
            self.assertNotWrapped()

    def testInitOnlyWrapsOnce(self):
        with platform('windows'):
            init()
            init()
            self.assertNotEqual(type(sys.stdout.wrapped), AnsiToWin32)
            self.assertNotEqual(type(sys.stderr.wrapped), AnsiToWin32)


if __name__ == '__main__':
    main()

