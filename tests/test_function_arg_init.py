"""
Test FunctionArgInit
"""

from collections import namedtuple

from arg_init import FunctionArgInit


Expected = namedtuple("Expected", "key value")


class TestFunctionArgInit:
    """
    Test function arguments are initialised
    """

    def test_function(self, fs):  # pylint: disable=unused-argument
        """
        Test FunctionArgInit
        """

        def test(arg1):  # pylint: disable=unused-argument
            """Test Class"""
            arg_init = FunctionArgInit()
            assert arg_init.args.arg1 == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
