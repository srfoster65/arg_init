"""
Test ArgInit with env over argument priority
"""

from collections import namedtuple
import logging

import pytest

# from arg_init import Arg
from arg_init import FunctionArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expected', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, argument, arg1_value, envs, expected",
        [
            # No Arg defined
            (None, {}, "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, {}, "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {}, None, {}, Expected("arg1", None)),

            # Use arg
            (None, {"name": "arg1"}, "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, {"name": "arg1", "default": "default"}, "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, {"name": "arg1", "default": "default", "force_arg": True}, None, {}, Expected("arg1", None)),
            (None, {"name": "arg1", "disable_env": True}, "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "arg1_value")),

            # Use env
            (None, {"name": "arg1"}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {"name": "arg1", "env": "ARG1", "default": "default"}, "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, {"name": "arg1", "env": "foo"}, "arg1_value", {"FOO": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", {"name": "arg1"}, None, {"PREFIX_ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", {"name": "arg1", "env": "ARG1"}, None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),

            # Use default
            (None, {"name": "arg1", "default": "default"}, None, {}, Expected("arg1", "default")),
            (None, {"name": "arg1", "default": "default"}, None, {"ARG1": ""}, Expected("arg1", "default")),
        ],
    )
    def test_matrix(self, prefix, argument, arg1_value, envs, expected):
        """
        Check combinations of args, envs and defaults.
        No Arg
        1. Use Arg
        2. Use Env
        3. Use default

        Env is used
        1. With default argument
        2. in preference to arg and default
        3. Env is renamed in Arg
        4. Prefix is set, env is undefined in Arg
        5. Prefix is set, env is defined in Arg
        6. Prefix is set, env is renamed in Arg
        7. Env is "" and used as force_env = True



        Arg is used
        1. With default argument, no env set
        2. In preference to default
        3. Renamed using attr
        4. Arg is None and used as force_arg = True

        Env is used
        1. With default argument
        2. in preference to arg and default
        3. Env is renamed in Arg
        4. Prefix is set, env is undefined in Arg
        5. Prefix is set, env is defined in Arg
        6. Prefix is set, env is renamed in Arg
        7. Env is "" and used as force_env = True
        
        Default is used
        1. Default is set in Arg
        2. Env is set, but disable_env = True
        """
        def test(arg1=None):
            arg_init = FunctionArgInit(env_prefix=prefix)
            if argument:
                arg_init.make_arg(**argument)
            args = arg_init.resolve()
            assert args[expected.key] == expected.value

        with pytest.MonkeyPatch.context() as mp:
            for env, value in envs.items():
                mp.setenv(env, value)
                test(arg1=arg1_value)

    def test_env_prefix(self):
        """
        Test env_prefix is applied to arg name        
        """
        def test(arg1):
            args = FunctionArgInit(env_prefix="prefix").resolve()
            assert args["arg1"] == env1_value

        env1 = "PREFIX_ARG1"
        env1_value = "env1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            arg1_value = "arg1_value"
            test(arg1_value)
            

    def test_multiple_args(self):
        """
        Test initialisation from args when no envs defined
        """
        def test(arg1, arg2):
            args = FunctionArgInit().resolve()
            assert args["arg1"] == arg1_value
            assert args["arg2"] == arg2_value

        arg1_value = "arg1_value"
        arg2_value = "p2_value"
        test(arg1_value, arg2_value)


    def test_multiple_envs(self):
        """
        Test initialised from envs
        """
        def test(arg1, arg2):
            args = FunctionArgInit().resolve()
            assert args["arg1"] == env1_value
            assert args["arg2"] == env2_value

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
          arg1 - env priority
          arg2 - env, arg = None
          arg3 - arg - env not set
        """
        def test(arg1, arg2, arg3):
            args =  FunctionArgInit().resolve()
            assert args["arg1"] == env1_value
            assert args["arg2"] == env2_value
            assert args["arg3"] == arg3_value

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        arg1_value = "arg1_arg"
        arg2_value = None
        arg3_value = "arg3_arg"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env2, env2_value)
            test(arg1_value, arg2_value, arg3_value)
