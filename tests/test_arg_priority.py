"""
Test ArgInit with argument priority
"""

from collections import namedtuple

import pytest

from arg_init import ArgDefaults
from arg_init import FunctionArgInit
from arg_init import Priority

Expected = namedtuple('Expected', 'key value')

# Custom priority order
PRIORITY_ORDER = (Priority.ARG, Priority.CONFIG, Priority.ENV, Priority.DEFAULT)

class TestArgPriority:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arg_value, envs, config, defaults, expected",
        [
            # Priority order
            (None, "arg1_value", {"ARG1": "env1_value"}, {"test": {"arg1": "config1_value"}}, [ArgDefaults(name="arg1", default_value="default")], Expected("arg1", "arg1_value")),
            (None, None, {"ARG1": "env1_value"}, {"test": {"arg1": "config1_value"}}, [ArgDefaults(name="arg1", default_value="default")], Expected("arg1", "config1_value")),
            (None, None, {"ARG1": "env1_value"}, {}, [ArgDefaults(name="arg1", default_value="default")], Expected("arg1", "env1_value")),
            (None, None, None, {}, [ArgDefaults(name="arg1", default_value="default")], Expected("arg1", "default")),
            (None, None, None, {}, None, Expected("arg1", None)),
        ],
    )
    def test_matrix(self, prefix, arg_value, envs, config, defaults, expected, fs):
        """
        Priority Order
        1. All defined - Arg is used
        2. Config, env and default defined - Config is used
        2. Env and default defined - Env is used
        3. Default is defined - Default is used
        4. Nothing defined - None is used
        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(env_prefix=prefix, defaults=defaults, priority=PRIORITY_ORDER).args
            assert args[expected.key] == expected.value

        fs.create_file("config.yaml", contents=str(config))
        with pytest.MonkeyPatch.context() as mp:
            if envs:
                for env, value in envs.items():
                    mp.setenv(env, value)
            test(arg1=arg_value)


    def test_false_values(self):
        """
        Test a logical false value sets the argument.
        """
        def test(arg1):  # pylint: disable=unused-argument
            arg1_defaults = ArgDefaults("arg1", default_value=1)
            args = FunctionArgInit(priority=PRIORITY_ORDER, defaults=[arg1_defaults]).args
            assert args["arg1"] == arg1_value

        arg1_value = 0
        test(arg1_value)


    def test_multiple_args(self):
        """
        Test multiple arg values
        """
        def test(arg1, arg2):  # pylint: disable=unused-argument
            args = FunctionArgInit(priority=PRIORITY_ORDER).args
            assert args["arg1"] == arg1_value
            assert args["arg2"] == arg2_value

        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
        test(arg1_value, arg2_value)

    def _test_multiple_config_args(self, fs):
        """
        Test multiple args defined in a config file
        """
        def test(arg1=None, arg2=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(priority=PRIORITY_ORDER).args
            assert args[arg1] == config1_value
            assert args[arg2] == config2_value

        arg1 = "arg1"
        config1_value = "config1_value"
        arg2 = "arg2"
        config2_value = "config2_value"
        config = {"test": {arg1: config1_value, arg2: config2_value}}
        fs.create_file("config.yaml", contents=str(config))
        test()

    def test_multiple_envs(self):
        """
        Test a multiple args from envs
        """
        def test(arg1=None, arg2=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(priority=PRIORITY_ORDER).args
            assert args["arg1"] == env1_value
            assert args["arg2"] == env2_value

        env1 = "ARG1"
        env1_value = "arg1_env"
        env2 = "ARG2"
        env2_value = "arg2_env"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            mp.setenv(env2, env2_value)
            test()

    def test_multiple_mixed(self):
        """
        Test mixed initialisation
          arg1 - arg priority
          arg2 - arg, env not set
          arg3 - eng - arg = None
        """
        def test(arg1, arg2, arg3):  # pylint: disable=unused-argument
            args = FunctionArgInit(priority=PRIORITY_ORDER).args
            assert args["arg1"] == arg1_value
            assert args["arg2"] == arg2_value
            assert args["arg3"] == env3_value

        env1 = "ARG1"
        env1_value = "arg1_env"
        env3 = "ARG3"
        env3_value = "env3_value"
        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
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
            args = FunctionArgInit(env_prefix="prefix", priority=PRIORITY_ORDER).args
            assert args["arg1"] == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
