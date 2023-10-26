"""
Test ArgInit with argument over env priority
"""

from collections import namedtuple
import logging

import pytest

from arg_init import Arg
from arg_init import ArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arguments, arg_value, envs, expected",
        [
            # No Arg defined
            (None, [], "arg1_value", {"ARG1": "env1_value"}, Expected("_arg1", "arg1_value")),
            (None, [], None, {"ARG1": "env1_value"}, Expected("_arg1", "env1_value")),
            (None, [], None, {}, Expected("_arg1", None)),

            # Use arg
            (None, [Arg("arg1", None, None, None, False, False, False)], "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, [Arg("arg1", None, "default", None, False, False, False)], "arg1_value", {"ARG": "env_value"}, Expected("arg1", "arg1_value")),
            (None, [Arg("arg1", None, "default", "new_arg", False, False, False)], "arg1_value", {"ARG": "env_value"}, Expected("new_arg", "arg1_value")),
            (None, [Arg("arg1", None, "default", None, True, False, False)], None, {"ARG1": "env_value"}, Expected("arg1", None)),

            # Use env
            (None, [Arg("arg1", None, None, None, False, False, False)], None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [Arg("arg1", "arg1", None, None, False, False, False)], None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [Arg("arg1", "foo", None, None, False, False, False)], None, {"FOO": "env1_value"}, Expected("arg1", "env1_value")),

            (None, [Arg("arg1", None, "default", None, False, True, False)], None, {"ARG1": ""}, Expected("arg1", "")),

            # Use default
            (None, [Arg("arg1", None, "default", None, False, False, False)], None, {}, Expected("arg1", "default")),
            (None, [Arg("arg1", None, "default", None, False, False, False)], None, {"ARG1": ""}, Expected("arg1", "default")),
            (None, [Arg("arg1", None, "default", None, False, False, True)], None, {"ARG1": "env_value"}, Expected("arg1", "default")),
        ],
    )
    def test_matrix(self, prefix, arguments, arg_value, envs, expected):
        """
        Check combinations of args, envs and defaults.
        No Arg
        1. Use Arg
        2. Use Env
        3. Use default
        
        Arg is used
        1. With default argument, no env set
        2. In preference to env and default
        3. Renamed using attr
        4. Arg is None and used as force_arg = True

        Env is used
        1. With default argument
        2. Env is defined same as arg in argument
        3. Env is renamed in argument
        4. Prefix is set, env is undefined in argument
        5. Prefix is set, env is defined in argument
        6. Prefix is set, env is renamed in argument
        7. Env is "" and used as force_env = True
        
        Default is used
        1. Default is set in argument
        2. Env is "" and is not used.
        3. Env is set, but disable_env = True
        """
        def _test(arg1=None):  # pylint: disable=unused-argument
            return ArgInit(env_prefix=prefix, priority=ArgInit.ARG_PRIORITY, args=arguments).args

        with pytest.MonkeyPatch.context() as mp:
            for env, value in envs.items():
                mp.setenv(env, value)
            args = _test(arg1=arg_value)
            assert args[expected.key].value == expected.value

    def test_multiple_args(self):
        """
        Test multiple arg values are returned
        """
        def _test(arg1, arg2):  # pylint: disable=unused-argument
            return ArgInit(priority=ArgInit.ARG_PRIORITY, protect_attrs=False).args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        arg2 = "arg2"
        arg2_value = "arg2_value"
        args = _test(arg1_value, arg2_value)
        assert args[arg1].value == arg1_value
        assert args[arg2].value == arg2_value


    def test_multiple_envs(self):
        """
        Test a multiple args can be initialised
        """
        def _test(arg1, arg2):  # pylint: disable=unused-argument
            return ArgInit(priority=ArgInit.ARG_PRIORITY, protect_attrs=False).args

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env2, env2_value)
            args = _test(None, None)
            assert args["arg1"].value == env1_value
            assert args["arg2"].value == env2_value

    def test_multiple_mixed(self):
        """
        Test mixed initialisation
          arg1 - arg priority
          arg2 - arg, env not set
          arg3 - eng - arg = None
        """
        def _test(arg1, arg2, arg3):  # pylint: disable=unused-argument
            return ArgInit(priority=ArgInit.ARG_PRIORITY, protect_attrs=False).args

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
            args = _test(arg1_value, arg2_value, arg3_value)
            assert args["arg1"].value == arg1_value
            assert args["arg2"].value == arg2_value
            assert args["arg3"].value == env3_value

    def test_env_prefix(self):
        """
        Test using env_prefix does not affect results
        """
        def _test(arg1):  # pylint: disable=unused-argument
            return ArgInit(env_prefix="prefix", priority=ArgInit.ARG_PRIORITY, protect_attrs=False).args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        args = _test(arg1_value)
        assert args[arg1].value == arg1_value
