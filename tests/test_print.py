"""
Test printing functions
"""

from arg_init import FunctionArgInit
from arg_init import ArgDefaults


class TestPrintFunctions:
    """
    Class to test default config .
    """

    def test_arg_str(self):
        """
        Test str() returns correct string
        """

        def test(arg1):
            args = FunctionArgInit().args
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
            args = FunctionArgInit().args
            out = repr(args[arg1_key])
            assert expected in out

        arg1_key = "arg1"
        arg1_value = "arg1_value"
        expected = (
            "<Arg("
            "name=arg1, env_name=ARG1, "
            "values=<Values(arg=arg1_value, env=None, default=None)>, "
            "value=arg1_value)"
        )

        test(arg1_value)

    def test_defaults_repr(self):
        """
        Test repr() returns correct string
        """

        arg1_defaults = ArgDefaults(
            name="arg1", default_value="default", env_name="ENV", disable_env="True"
        )
        defaults = [arg1_defaults]
        out = repr(defaults)
        expected = (
            "<ArgDefaults("
            "name=arg1, "
            "default_value=default, "
            "env_name=ENV, "
            "disable_env=True)"
        )
        assert expected in out
