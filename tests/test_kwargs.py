"""
Test ArgInit processes kwargs.
"""

from collections import namedtuple
import logging

from arg_init import ArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    def test_kwargs_not_used(self):
        """
        Test kwargs are ignored if not explicity enabled
        """
        def _test(arg1, **kwargs):
            return ArgInit().args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        kwarg1 = "kwarg1"
        kwarg1_value = "kwarg1_value"
        kwargs = {kwarg1: kwarg1_value}
        args = _test(arg1_value, **kwargs)
        assert args[arg1] == arg1_value
        assert kwarg1 not in args


    def test_kwargs_used(self):
        """
        Test kwargs are processed if enabled
        """
        def _test(arg1, **kwargs):
            return ArgInit(use_kwargs=True).args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        kwarg1 = "kwarg1"
        kwarg1_value = "kwarg1_value"
        kwargs = {kwarg1: kwarg1_value}
        args = _test(arg1_value, **kwargs)
        assert args[arg1] == arg1_value
        assert args[kwarg1] == kwarg1_value
