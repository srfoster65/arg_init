"""
Test ArgInit with env priority
"""

from collections import namedtuple

import pytest


from arg_init import FunctionArgInit, ArgDefaults, Priority


Expected = namedtuple("Expected", "key value")


# Common test defaults
PRIORITY_ORDER = (Priority.ARG, Priority.CONFIG, Priority.ENV, Priority.DEFAULT)
ENV = {"ARG1": "env1_value"}
CONFIG = '{"test": {"arg1": "config1_value"}}'
DEFAULTS = [ArgDefaults(name="arg1", default_value="default")]


class TestEnvPriority:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arg_value, envs, config, defaults, expected",
        [
            (None, "arg1_value", ENV, CONFIG, DEFAULTS, Expected("arg1", "config1_value")),
            (None, "arg1_value", ENV, {}, DEFAULTS, Expected("arg1", "env1_value")),
            (None, "arg1_value", None, {}, DEFAULTS, Expected("arg1", "env1_value")),
            (None, None, None, {}, DEFAULTS, Expected("arg1", "default")),
            (None, None, None, {}, None, Expected("arg1", None)),
        ],
    )
    def test_priority(self, prefix, arg_value, envs, config, defaults, expected, fs):
        """
        Priority Order
        1. All defined - Env is used
        2. Arg and default defined - Arg is used
        3. Default is defined - Default is used
        4. Nothing defined - None is used
        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(env_prefix=prefix, defaults=defaults).args
            assert args[expected.key] == expected.value

        fs.create_file("config.yaml", contents=str(config))
        with pytest.MonkeyPatch.context() as mp:
            if envs:
                for env, value in envs.items():
                    mp.setenv(env, value)
                test(arg1=arg_value)

    def test_function_default(self, fs):  # pylint: disable=unused-argument
        """
        Test function default is used if set and no arg passed in.
        """

        def test(arg1="func_default"):  # pylint: disable=unused-argument
            defaults = [ArgDefaults(name="arg1", default_value="default")]
            args = FunctionArgInit(defaults=defaults).args
            assert args["arg1"] == "func_default"

        test()

    def test_multiple_args(self, fs):  # pylint: disable=unused-argument
        """
        Test initialisation from args when no envs defined
        """

        def test(arg1, arg2):  # pylint: disable=unused-argument
            """Test Class"""
            args = FunctionArgInit().args
            assert args["arg1"] == arg1_value
            assert args["arg2"] == arg2_value

        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
        test(arg1_value, arg2_value)

    def test_multiple_envs(self, fs):  # pylint: disable=unused-argument
        """
        Test initialised from envs
        """

        def test(arg1, arg2):  # pylint: disable=unused-argument
            """Test Class"""
            args = FunctionArgInit().args
            assert args["arg1"] == env1_value
            assert args["arg2"] == env2_value

        env1 = "ARG1"
        env1_value = "env1_value"
        env2 = "ARG2"
        env2_value = "env2_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env2, env2_value)
            test("arg1_value", "arg2_value")

    def test_multiple_mixed(self, fs):  # pylint: disable=unused-argument
        """
        Test mixed initialisation
          arg1 - env priority
          arg2 - env, arg = None
          arg3 - arg - env not set
        """

        def test(arg1, arg2, arg3):  # pylint: disable=unused-argument
            """Test Class"""
            args = FunctionArgInit().args
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
