"""
Test printing functions
"""

import logging

from arg_init import ArgInit
from arg_init import Arg


logger = logging.getLogger(__name__)


class TestPrintFunctions:
    """
    Class to test default config .
    """

    def test_str(self):
        """
        Test first line of str() returns correct string
        """

        def _test(arg1):
            return ArgInit().args

        arg1 = "_arg1"
        arg1_value = "arg1_value"
        expected = arg1_value
        args = _test(arg1_value)
        out = str(args[arg1])
        assert expected in out

    def test_repr(self):
        """
        Test repr() returns correct string
        """

        def _test(arg1):
            return ArgInit().args

        arg1 = "_arg1"
        arg1_value = "arg1_value"
        expected = "<Arg("\
                   "arg=<Attribute(name=arg1, value=arg1_value, force=False)>, "\
                   "env=<Attribute(name=ARG1, value=None, force=False)>, "\
                   "default=<Attribute(name=default, value=None, force=True)>, "\
                   "attr=_arg1, disable_env=False, priority=env_priority, value=arg1_value)>"
        args = _test(arg1_value)
        out = repr(args[arg1])
        assert expected in out
