"""
Test ArgInit processes kwargs.
"""

from collections import namedtuple
import logging

from arg_init import ArgInit
# from arg_init import Arg


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestEdgeCases:
    """
    Class to test ArgInit for argument priority.
    """

    def test_arg_not_found(self):
        """
        Test no action taken if no Arg available
        """
        def _test(arg1):
            arg_init = ArgInit()
            args = arg_init.resolve(args=[arg_init.make_arg("arg2")])
            assert args[arg1_name] == arg1

        arg1_name = "_arg1"
        arg1_value = "arg1_value"
        _test(arg1_value)
