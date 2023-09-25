"""
Test default logging configuration.
"""

from collections import namedtuple
import logging

import pytest

from arg_init import Arg
from arg_init.args import ArgInit

from .environ import modified_environ


logger = logging.getLogger(__name__)


Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, param, arg_value, envs, expected",
        [
            # No Arg defined
            (None, None, "arg_value", {"ARG": "env_value"}, Expected("arg", "arg_value")),
            (None, None, None, {"ARG": "env_value"}, Expected("arg", "env_value")),
            (None, None, None, {}, Expected("arg", None)),

            # Use arg
            (None, Arg("arg", None, None, None, False, False, True, False), "arg_value", {}, Expected("arg", "arg_value")),
            (None, Arg("arg", None, "default", None, False, False, True, False), "arg_value", {"ARG": "env_value"}, Expected("arg", "arg_value")),
            (None, Arg("arg", None, "default", "new_arg", False, False, True, False), "arg_value", {"ARG": "env_value"}, Expected("new_arg", "arg_value")),
            (None, Arg("arg", None, "default", None, True, False, True, False), None, {"ARG": "env_value"}, Expected("arg", None)),

            # Use env
            (None, Arg("arg", None, None, None, False, False, True, False), None, {"ARG": "env_value"}, Expected("arg", "env_value")),
            (None, Arg("arg", "arg", None, None, False, False, True, False), None, {"ARG": "env_value"}, Expected("arg", "env_value")),
            (None, Arg("arg", "foo", None, None, False, False, True, False), None, {"foo": "env_value"}, Expected("arg", "env_value")),
            ("prefix", Arg("arg", None, None, None, False, False, True, False), None, {"PREFIX_ARG": "env_value"}, Expected("arg", "env_value")),
            ("prefix", Arg("arg", "arg", None, None, False, False, True, False), None, {"PREFIX_ARG": "env_value"}, Expected("arg", "env_value")),
            ("prefix", Arg("arg", "foo", None, None, False, False, True, False), None, {"PREFIX_FOO": "env_value"}, Expected("arg", "env_value")),
            (None, Arg("arg", None, "default", None, False, True, False, False), None, {"ARG": ""}, Expected("arg", "")),

            # Use default
            (None, Arg("arg", None, "default", None, False, False, True, False), None, {}, Expected("arg", "default")),
            (None, Arg("arg", None, "default", None, False, False, True, True), None, {"ARG": "env_value"}, Expected("arg", "default")),
        ],
    )
    def test_matrix(self, prefix, param, arg_value, envs, expected):
        """
        Check combinations of args, envs and defaults.
        No Arg
        1. Use Arg
        2. Use Env
        3. Use default
        
        Arg is used
        1. With default param, no env set
        2. In preference to env and default
        3. Renamed using attr
        4. Arg is None and used as force_arg = True

        Env is used
        1. With default param
        2. Env is defined same as arg in param
        3. Env is renamed in param
        4. Prefix is set, env is undefined in param
        5. Prefix is set, env is defined in param
        6. Prefix is set, env is renamed in param
        7. Env is "" and used as force_env = True
        
        Default is used
        1. Default is set in param
        2. Env is set, but disable_env = True
        """
        def _test(arg=None):
            print(param)
            params = [param] if param else []
            return ArgInit(env_prefix=prefix).go(params).args

        # envs = envs if envs else {}
        with modified_environ(**envs):
            params = _test(arg=arg_value)
            assert params[expected.key] == expected.value


    def test_multiple_params(self):
        """
        Test multiple param values are returned
        """
        def _test(arg1, arg2):
            return ArgInit().go().args

        arg1 = "arg1"
        arg1_value = "arg1_value"
        arg2 = "arg2"
        arg2_value = "p2_value"
        params = _test(arg1_value, arg2_value)
        assert params[arg1] == arg1_value
        assert params[arg2] == arg2_value


    def test_multiple_envs(self):
        """
        Test a multiple params can be initialised
        """
        def _test(arg1, arg2):
            return ArgInit().go().args

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        envs = {env1: env1_value, env2: env2_value}
        with modified_environ(**envs):
            params = _test(None, None)
            assert params["arg1"] == env1_value
            assert params["arg2"] == env2_value

