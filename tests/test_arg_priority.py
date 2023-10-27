"""
Test ArgInit with argument over env priority
"""

from collections import namedtuple
import logging

import pytest

# from arg_init import Arg
from arg_init import FunctionArgInit
from arg_init import ARG_PRIORITY

logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, argument, arg_value, envs, expected",
        [
            # No Arg defined
            (None, {}, "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "arg1_value")),
            (None, {}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {}, None, {}, Expected("arg1", None)),

            # Use arg
            (None, {"name": "arg1"}, "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, {"name": "arg1", "default": "default"}, "arg1_value", {"ARG": "env_value"}, Expected("arg1", "arg1_value")),
            (None, {"name": "arg1", "default": "default", "force_arg": True}, None, {"ARG1": "env_value"}, Expected("arg1", None)),
            (None, {"name": "arg1", "disable_env": True}, "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "arg1_value")),


            # Use env
            (None, {"name": "arg1"}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {"name": "arg1", "env": "ARG1"}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {"name": "arg1", "env": "foo"}, None, {"FOO": "env1_value"}, Expected("arg1", "env1_value")),

            ("prefix", {"name": "arg1"}, None, {"PREFIX_ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", {"name": "arg1", "env": "ARG1"}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),

            (None, {"name": "arg1", "force_env": True}, None, {"ARG1": ""}, Expected("arg1", "")),

            # Use default
            (None, {"name": "arg1", "default": "default"}, None, {}, Expected("arg1", "default")),
            (None, {"name": "arg1", "default": "default"}, None, {"ARG1": ""}, Expected("arg1", "default")),
        ],
    )
    def test_matrix(self, prefix, argument, arg_value, envs, expected):
        """
        Check combinations of args, envs and defaults.
        No Args
        1. Use Arg
        2. Use Env
        3. Use default
        
        Arg is used
        1. With default argument, no env set
        2. In preference to env and default
        3. Arg is None and used as force_arg = True
        4. Env is set but disable_env=True

        Env is used
        1. With default argument
        2. Env is defined same as arg in argument
        3. Env is renamed in argument
        4. Prefix is set, env is undefined in argument
        5. Prefix is set, env is defined in argument
        6. Env is "" and used as force_env = True
        
        Default is used
        1. Default is set in argument
        2. Env is "" and is not used.
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            arg_init = FunctionArgInit(env_prefix=prefix)
            if argument:
                arg_init.make_arg(**argument)
            args = arg_init.resolve(priority=ARG_PRIORITY)
            assert args[expected.key].value == expected.value

        with pytest.MonkeyPatch.context() as mp:
            for env, value in envs.items():
                mp.setenv(env, value)
            test(arg1=arg_value)
            

    def test_multiple_args(self):
        """
        Test multiple arg values are returned
        """
        def test(arg1, arg2):  # pylint: disable=unused-argument
            args = FunctionArgInit().resolve(priority=ARG_PRIORITY)
            assert args["arg1"].value == arg1_value
            assert args["arg2"].value == arg2_value

        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
        test(arg1_value, arg2_value)


    def test_multiple_envs(self):
        """
        Test a multiple args can be initialised
        """
        def test(arg1, arg2):  # pylint: disable=unused-argument
            args = FunctionArgInit().resolve(priority=ARG_PRIORITY)
            assert args["arg1"].value == env1_value
            assert args["arg2"].value == env2_value

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env2, env2_value)
            test(None, None)

    def test_multiple_mixed(self):
        """
        Test mixed initialisation
          arg1 - arg priority
          arg2 - arg, env not set
          arg3 - eng - arg = None
        """
        def test(arg1, arg2, arg3):  # pylint: disable=unused-argument
            args = FunctionArgInit().resolve(priority=ARG_PRIORITY)
            assert args["arg1"].value == arg1_value
            assert args["arg2"].value == arg2_value
            assert args["arg3"].value == env3_value

        env1 = "ARG1"
        env1_value = "arg1_env"
        env3 = "ARG3"
        env3_value = "arg3_env"
        arg1_value = "arg1_arg"
        arg2_value = "arg1_arg"
        arg3_value = None
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env3, env3_value)
            test(arg1_value, arg2_value, arg3_value)

    def test_env_prefix(self):
        """
        Test using env_prefix does not affect results
        """
        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(env_prefix="prefix").resolve(priority=ARG_PRIORITY)
            assert args["arg1"].value == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
