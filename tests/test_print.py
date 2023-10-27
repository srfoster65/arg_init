"""
Test printing functions
"""

import logging

from arg_init import FunctionArgInit


logger = logging.getLogger(__name__)


class TestPrintFunctions:
    """
    Class to test default config .
    """

    def test_arg_str(self):
        """
        Test str() returns correct string
        """

        def test(arg1):
            args = FunctionArgInit().resolve()
            out = str(args[arg1_key])
            assert expected in out

        arg1_key = "arg1"
        arg1_value = "arg1_value"
        expected = arg1_value
        test(arg1_value)

    def test_arg_repr(self):
        """
        Test repr() returns correct string
        """

        def test(arg1):
            args = FunctionArgInit().resolve()
            out = repr(args[arg1_key])
            assert expected in out

        arg1_key = "arg1"
        arg1_value = "arg1_value"
        expected = "<Arg("\
                   "arg=<Attribute(name=arg1, value=arg1_value, force=False)>, "\
                   "env=<Attribute(name=ARG1, value=None, force=False)>, "\
                   "default=<Attribute(name=default, value=None, force=True)>, "\
                   "disable_env=False, priority=env_priority, value=arg1_value)>"
        test(arg1_value)
