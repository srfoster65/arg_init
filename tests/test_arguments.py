"""
Test ArgDefaults
"""

from collections import namedtuple
import logging

import pytest

from arg_init import ClassArgInit, FunctionArgInit, ArgDefaults, Priority

logger = logging.getLogger(__name__)
Expected = namedtuple("Expected", "key value")


# Common test defaults
PRIORITY_ORDER = (Priority.ARG, Priority.CONFIG, Priority.ENV, Priority.DEFAULT)
ENV = {"ARG1": "env1_value"}
CONFIG = '{"test": {"arg1": "config1_value"}}'
DEFAULTS = [ArgDefaults(name="arg1", default_value="default")]


class TestArguments:
    """
    Class to test arguments are initialised correctly.
    """

    @pytest.mark.parametrize(
        "arg_value, envs, config, defaults, expected",
        [
            # Priority order
            (0, None, None, DEFAULTS, Expected("arg1", 0)),
            ("", None, None, DEFAULTS, Expected("arg1", "")),
            (None, {"ARG1": ""}, None, DEFAULTS, Expected("arg1", "")),
            (None, None, '{"test": {"arg1": 0}}', DEFAULTS, Expected("arg1", 0)),
            (None, None, '{"test": {"arg1": ""}}', DEFAULTS, Expected("arg1", "")),
        ],
    )
    def test_logical_false_values(self, arg_value, envs, config, defaults, expected, fs):
        """
        Priority Order
        1. Test 0 argument
        2. Test "" argument
        2. Test "" env. Note env only supports string
        3. Test 0 config
        4. Test "" config
        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(defaults=defaults, priority=PRIORITY_ORDER).args
            print(args[expected.key], expected.value)
            assert args[expected.key] == expected.value

        if config:
            fs.create_file("config.yaml", contents=config)
        with pytest.MonkeyPatch.context() as mp:
            if envs:
                for env, value in envs.items():
                    mp.setenv(env, value)
            test(arg1=arg_value)

    def test_default_value(self):
        """
        Test setting a default_value
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):  # pylint: disable=unused-argument
                name = "arg1"
                default_value = "arg1_default"
                defaults = [ArgDefaults(name=name, default_value=default_value)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.values.default == default_value

        Test()

    def test_env_name(self):
        """
        Test setting an explicit an env_name
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):  # pylint: disable=unused-argument
                name = "arg1"
                alt_name = "ENV1"
                defaults = [ArgDefaults(name=name, alt_name=alt_name)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.env_name == alt_name

        Test()
