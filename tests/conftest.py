import sys


def pytest_ignore_collect(path):
    return sys.version_info[0] <= 2 and str(path).endswith("__py3.py")
