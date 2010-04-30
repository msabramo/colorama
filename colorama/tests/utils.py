# Copyright (c) 2010 Jonathan Hartley <tartley@tartley.com>
# See LICENSE.txt

from contextlib import contextmanager
import sys

@contextmanager
def platform(name):
    orig = sys.platform
    sys.platform = name
    yield
    sys.platform = orig

