"""
Test ArgInit with env over argument priority
"""

from collections import namedtuple
import logging

import pytest

from arg_init import Arg
from arg_init import ArgInit

from .environ import modified_environ


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arguments, arg1_value, envs, expected",
        [
            # No Arg defined
            (None, [], "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, [], "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [], None, {}, Expected("arg1", None)),

            # Use arg
            (None, [Arg("arg1", None, None, None, False, False, True, False)], "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, [Arg("arg1", None, "default", None, False, False, True, False)], "arg1_value", {}, Expected("arg1", "arg1_value")),
            (None, [Arg("arg1", None, "default", "new_arg", False, False, True, False)], "arg1_value", {}, Expected("new_arg", "arg1_value")),
            (None, [Arg("arg1", None, "default", None, True, False, True, False)], None, {}, Expected("arg1", None)),

            # Use env
            (None, [Arg("arg1", None, None, None, False, False, True, False)], None, {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [Arg("arg1", "arg1", None, None, False, False, True, False)], "arg1_value", {"ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [Arg("arg1", "foo", None, None, False, False, True, False)], "arg1_value", {"FOO": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", [Arg("arg1", None, None, None, False, False, True, False)], "arg1_value", {"PREFIX_ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", [Arg("arg1", "arg1", None, None, False, False, True, False)], "arg1_value", {"PREFIX_ARG1": "env1_value"}, Expected("arg1", "env1_value")),
            ("prefix", [Arg("arg1", "foo", None, None, False, False, True, False)], "arg1_value", {"PREFIX_FOO": "env1_value"}, Expected("arg1", "env1_value")),
            (None, [Arg("arg1", None, "default", None, False, True, False, False)], "arg1_value", {"ARG1": ""}, Expected("arg1", "")),

            # Use default
            (None, [Arg("arg1", None, "default", None, False, False, True, False)], None, {}, Expected("arg1", "default")),
            (None, [Arg("arg1", None, "default", None, False, False, True, True)], None, {"ARG1": "env1_value"}, Expected("arg1", "default")),
        ],
    )
    def test_matrix(self, prefix, arguments, arg1_value, envs, expected):
        """
        Check combinations of args, envs and defaults.
        No Arg
        1. Use Arg
        2. Use Env
        3. Use default
        
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
        def _test(arg1=None):
            return ArgInit(env_prefix=prefix, priority=ArgInit.ENV_PRIORITY, args=arguments).args

        with modified_environ(**envs):
            args = _test(arg1=arg1_value)
            assert args[expected.key] == expected.value


    def test_multiple_args(self):
        """
        Test multiple arg values are returned
        """
        def _test(arg1, arg2):
            return ArgInit().args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        arg2 = "arg2"
        arg2_value = "p2_value"
        args = _test(arg1_value, arg2_value)
        assert args[arg1] == arg1_value
        assert args[arg2] == arg2_value


    def test_multiple_envs(self):
        """
        Test a multiple args can be initialised
        """
        def _test(arg1, arg2):
            return ArgInit().args

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        envs = {env1: env1_value, env2: env2_value}
        with modified_environ(**envs):
            args = _test(None, None)
            assert args["arg1"] == env1_value
            assert args["arg2"] == env2_value
