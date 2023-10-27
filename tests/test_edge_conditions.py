"""
Test ArgInit processes kwargs.
"""

from collections import namedtuple
import logging

from arg_init import FunctionArgInit


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
        def test(arg1):
            arg_init = FunctionArgInit()
            arg_init.make_arg("arg2")
            args = arg_init.resolve()
            assert args["arg1"] == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
