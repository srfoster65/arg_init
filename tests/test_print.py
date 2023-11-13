"""
Test printing functions
"""

from arg_init import FunctionArgInit, ArgDefaults


class TestPrintFunctions:
    """
    Class to test default config .
    """

    def test_arg_str(self, fs):  # pylint: disable=unused-argument
        """
        Test str() returns correct string
        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit().args
            out = str(args[arg1_key])
            assert expected in out

        arg1_key = "arg1"
        arg1_value = "arg1_value"
        expected = arg1_value
        test(arg1_value)

    def test_arg_repr(self, fs):  # pylint: disable=unused-argument
        """
        Test repr() returns correct string
        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit().args
            out = repr(args[arg1_key])
            assert expected in out

        arg1_key = "arg1"
        arg1_value = "arg1_value"
        expected = (
            "<Arg("
            "name=arg1, env_name=ARG1, config_name=arg1, "
            "values=<Values(arg=arg1_value, env=None, config=None, default=None)>, "
            "value=arg1_value)>"
        )

        test(arg1_value)

    def test_defaults_repr(self, fs):  # pylint: disable=unused-argument
        """
        Test repr() returns correct string
        """

        arg1_defaults = ArgDefaults(name="arg1", default_value="default", alt_name="ENV")
        defaults = [arg1_defaults]
        out = repr(defaults)
        expected = "<ArgDefaults(name=arg1, default_value=default, alt_name=ENV)>"
        assert expected in out
