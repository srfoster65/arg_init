"""
Test ArgInit processes kwargs.
"""

from collections import namedtuple
import logging

from arg_init import ArgInit
from arg_init import Arg


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    def test_arg_not_found(self):
        """
        Test no action taken if no Arg available
        """
        def _test(arg1):
            return ArgInit(args=[Arg("arg2")]).args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        args = _test(arg1_value)
        assert args[arg1] == arg1_value


    def test_arg_not_set(self):
        """
        Test is no arg, env or default set and force_default=False
        arg is not set in args.
        """
        def _test(arg1):
            return ArgInit(args=[Arg("arg1", force_default=False)]).args

        arg1 = "arg1"
        arg1_value = None
        args = _test(arg1_value)
        assert arg1 not in args
