"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

import pytest

from arg_init import ClassArgInit

logger = logging.getLogger(__name__)
Expected = namedtuple("Expcted", "key value")


class TestArgFactory:
    """
    Test Args are initialised correctly by the Arg Factory
    """

    def test_single_arg(self):
        """
        Test factory created arg
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1):
                arg_init = ClassArgInit()
                arg_init.make_arg(name="arg1")
                arg_init.resolve()
                assert arg_init.args.arg1 == arg1_value
                assert self._arg1 == arg1_value

        arg1_value = "arg1_value"
        Test(arg1_value)

    def test_env_prefix_arg(self):
        """
        Test factory created arg sets env prefix
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1):
                arg_init = ClassArgInit(env_prefix="prefix")
                arg_init.make_arg(name=arg1)
                arg_init.resolve()
                assert arg_init.args.arg1 == env1_value
                assert self._arg1 == env1_value

        env1 = "PREFIX_ARG1"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            Test(arg1_value)

    def test_protect_false_arg(self):
        """
        Test factory created Arg sets arg name
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1):
                arg_init = ClassArgInit()
                arg_init.make_arg(arg1)
                arg_init.resolve(protect_args=False)
                assert arg_init.args.arg1 == arg1_value
                assert self.arg1 == arg1_value

        arg1_value = "arg1_value"
        Test(arg1_value)

    def test_multiple_args(self):
        """
        Test mutiple args are created
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1, arg2):
                arg_init = ClassArgInit()
                arg_init.make_arg("arg1")
                arg_init.make_arg("arg2")
                arg_init.resolve()
                assert arg_init.args.arg1 == arg1_value
                assert arg_init.args.arg2 == arg2_value

        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
        Test(arg1_value, arg2_value)
