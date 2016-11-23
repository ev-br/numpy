"""
Decorators for labeling and modifying behavior of test objects.

Decorators that merely return a modified version of the original
function object are straightforward. Decorators that return a new
function object need to use
::

  nose.tools.make_decorator(original_function)(decorator)

in returning the decorator, in order to preserve meta-data such as
function name, setup and teardown functions and so on - see
``nose.tools`` for more information.

"""
from __future__ import division, absolute_import, print_function

import collections

from .utils import SkipTest, assert_warns


def slow(t):
    """
    Label a test as 'slow'.

    The exact definition of a slow test is obviously both subjective and
    hardware-dependent, but in general any individual test that requires more
    than a second or two should be labeled as slow (the whole suite consits of
    thousands of tests, so even a second is significant).

    Parameters
    ----------
    t : callable
        The test to label as slow.

    Returns
    -------
    t : callable
        The decorated test `t`.

    Examples
    --------
    The `numpy.testing` module includes ``import decorators as dec``.
    A test can be decorated as slow like this::

      from numpy.testing import *

      @dec.slow
      def test_big(self):
          print('Big, slow test')

    """

#    t.slow = True
#    return t
    import pytest
    return pytest.mark.skipif(not pytest.config.getoption("--full"),
                              reason="need --full option to run.")


def setastest(tf=True):
    """
    Signals to nose that this function is or is not a test.

    Parameters
    ----------
    tf : bool
        If True, specifies that the decorated callable is a test.
        If False, specifies that the decorated callable is not a test.
        Default is True.

    Notes
    -----
    This decorator can't use the nose namespace, because it can be
    called from a non-test module. See also ``istest`` and ``nottest`` in
    ``nose.tools``.

    Examples
    --------
    `setastest` can be used in the following way::

      from numpy.testing.decorators import setastest

      @setastest(False)
      def func_with_test_in_name(arg1, arg2):
          pass

    """
    def set_test(t):
        t.__test__ = tf
        return t
    return set_test

def skipif(skip_condition, msg=None):
    """
    Make function raise SkipTest exception if a given condition is true.

    If the condition is a callable, it is used at runtime to dynamically
    make the decision. This is useful for tests that may require costly
    imports, to delay the cost until the test suite is actually executed.

    Parameters
    ----------
    skip_condition : bool or callable
        Flag to determine whether to skip the decorated test.
    msg : str, optional
        Message to give on raising a SkipTest exception. Default is None.

    Returns
    -------
    decorator : function
        Decorator which, when applied to a function, causes SkipTest
        to be raised when `skip_condition` is True, and the function
        to be called normally otherwise.

    Notes
    -----
    The decorator itself is decorated with the ``nose.tools.make_decorator``
    function in order to transmit function name, and various other metadata.

    """
    import pytest
    return pytest.mark.skipif(skip_condition, reason=msg)


def knownfailureif(fail_condition, msg=None):
    """
    Make function raise KnownFailureException exception if given condition is true.

    If the condition is a callable, it is used at runtime to dynamically
    make the decision. This is useful for tests that may require costly
    imports, to delay the cost until the test suite is actually executed.

    Parameters
    ----------
    fail_condition : bool or callable
        Flag to determine whether to mark the decorated test as a known
        failure (if True) or not (if False).
    msg : str, optional
        Message to give on raising a KnownFailureException exception.
        Default is None.

    Returns
    -------
    decorator : function
        Decorator, which, when applied to a function, causes
        KnownFailureException to be raised when `fail_condition` is True,
        and the function to be called normally otherwise.

    Notes
    -----
    The decorator itself is decorated with the ``nose.tools.make_decorator``
    function in order to transmit function name, and various other metadata.

    """
    import pytest
    return pytest.mark.xfail(fail_condition, reason=msg)


def deprecated(conditional=True):
    """
    Filter deprecation warnings while running the test suite.

    This decorator can be used to filter DeprecationWarning's, to avoid
    printing them during the test suite run, while checking that the test
    actually raises a DeprecationWarning.

    Parameters
    ----------
    conditional : bool or callable, optional
        Flag to determine whether to mark test as deprecated or not. If the
        condition is a callable, it is used at runtime to dynamically make the
        decision. Default is True.

    Returns
    -------
    decorator : function
        The `deprecated` decorator itself.

    Notes
    -----
    .. versionadded:: 1.4.0

    """
    def deprecate_decorator(f):
        # Local import to avoid a hard nose dependency and only incur the
        # import time overhead at actual test-time.
        import nose

        def _deprecated_imp(*args, **kwargs):
            # Poor man's replacement for the with statement
            with assert_warns(DeprecationWarning):
                f(*args, **kwargs)

        if isinstance(conditional, collections.Callable):
            cond = conditional()
        else:
            cond = conditional
        if cond:
            return nose.tools.make_decorator(f)(_deprecated_imp)
        else:
            return f
    return deprecate_decorator
