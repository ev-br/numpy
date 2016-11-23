# 
# Provide a @slow decorator, after
# http://doc.pytest.org/en/latest/example/simple.html#dynamically-adding-command-line-options
#
# the decorator itself is defined in testing/decorators.py

import pytest
def pytest_addoption(parser):
    parser.addoption("--full", action="store_true",
        help="run slow tests, too")
