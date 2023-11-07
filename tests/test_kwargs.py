"""
Test ArgInit processes kwargs.
"""

from collections import namedtuple

from arg_init import ClassArgInit
from arg_init import FunctionArgInit


Expected = namedtuple('Expcted', 'key value')


class TestKwargs:
    """
    Class to test ArgInit for argument priority.
    """

    def test_kwargs_not_used(self, fs):
        """
        Test kwargs are ignored if not explicity enabled
        """
        def test(arg1, **kwargs):
            """Test Class"""
            args = FunctionArgInit(use_kwargs=True).args
            assert args["arg1"] == arg1_value
            assert "_kwarg1" not in args

        arg1_value = "arg1_value"
        kwarg1 = "kwarg1"
        kwarg1_value = "kwarg1_value"
        kwargs = {kwarg1: kwarg1_value}
        test(arg1_value, **kwargs)


    def test_kwargs_used_for_function(self, fs):
        """
        Test kwargs are processed if enabled
        """
        def test(arg1, **kwargs):
            """Test Class"""
            args = FunctionArgInit(use_kwargs=True).args
            assert args["arg1"] == arg1_value
            assert args["kwarg1"] == kwarg1_value

        arg1_value = "arg1_value"
        kwarg1 = "kwarg1"
        kwarg1_value = "kwarg1_value"
        kwargs = {kwarg1: kwarg1_value}
        test(arg1_value, **kwargs)


    def test_kwargs_used_for_class(self, fs):
        """
        Test kwargs are processed if enabled
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1, **kwargs):
                args = ClassArgInit(use_kwargs=True).args
                assert args["arg1"] == arg1_value
                assert args["kwarg1"] == kwarg1_value

        arg1_value = "arg1_value"
        kwarg1 = "kwarg1"
        kwarg1_value = "kwarg1_value"
        kwargs = {kwarg1: kwarg1_value}
        Test(arg1_value, **kwargs)
