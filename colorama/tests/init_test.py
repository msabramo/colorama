
import sys
from unittest2 import TestCase, main

from mock import Mock, patch

from .utils import platform

from .. import init, AnsiToWin32

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

    def testInitAutoresetOnWrapsOnAllPlatforms(self):
        with platform('darwin'):
            init(autoreset=True)
            self.assertWrapped()

    def testInitWrapOffDoesntWrapOnWindows(self):
        with platform('windows'):
            init(wrap=False)
            self.assertNotWrapped()

    def testInitWrapOffIncompatibleWithAutoresetOn(self):
        self.assertRaises( ValueError, lambda: init(autoreset=True, wrap=False) )

    def testInitOnlyWrapsOnce(self):
        with platform('windows'):
            init()
            init()
            self.assertWrapped()

    def testAutoResetPassedOn(self):
        init(autoreset=True)
        self.assertTrue( sys.stdout.autoreset )
        self.assertTrue( sys.stderr.autoreset )

    def testAutoResetChangeable(self):
        init()
        init(autoreset=True)
        self.assertWrapped()
        self.assertTrue( sys.stdout.autoreset )
        self.assertTrue( sys.stderr.autoreset )
        init()
        self.assertWrapped()
        self.assertFalse( sys.stdout.autoreset )
        self.assertFalse( sys.stderr.autoreset )


if __name__ == '__main__':
    main()

