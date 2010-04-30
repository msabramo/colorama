
from contextlib import contextmanager
import sys

@contextmanager
def platform(name):
    orig = sys.platform
    sys.platform = name
    yield
    sys.platform = orig

