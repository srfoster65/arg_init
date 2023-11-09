"""
Test priority sequences
"""

from collections import namedtuple

import pytest

from arg_init import (
    FunctionArgInit,
    ArgDefaults,
    Priority,
    ENV_PRIORITY,
    CONFIG_PRIORITY,
    ARG_PRIORITY,
)


Expected = namedtuple("Expected", "key value")

# Common test defaults
ENV = {"ARG1": "env1_value"}
CONFIG = '{"test": {"arg1": "config1_value"}}'
DEFAULTS = [ArgDefaults(name="arg1", default_value="default")]


class TestPrioritySequences:
    """
    Class to test ArgInit for argument priority.
    """

    def test_config_priority(self, fs):  # pylint: disable=unused-argument
        """
        Test config priority
        """

        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(priorities=CONFIG_PRIORITY).args
            assert args["arg1"] == config1_value

        fs.create_file("config.yaml", contents=CONFIG)
        env1 = "ARG1"
        config1_value = "config1_value"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            test(arg1_value)

    def test_env_priority(self, fs):  # pylint: disable=unused-argument
        """
        Test config priority
        """

        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(priorities=ENV_PRIORITY).args
            assert args["arg1"] == env1_value

        fs.create_file("config.yaml", contents=CONFIG)
        env1 = "ARG1"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            test(arg1_value)

    def test_arg_priority(self, fs):  # pylint: disable=unused-argument
        """
        Test config priority
        """

        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(priorities=ARG_PRIORITY).args
            assert args["arg1"] == arg1_value

        fs.create_file("config.yaml", contents=CONFIG)
        env1 = "ARG1"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            test(arg1_value)

    def test_custom_priority(self, fs):  # pylint: disable=unused-argument
        """
        Test config priority
        """

        def test(arg1=None):  # pylint: disable=unused-argument
            priorities = (Priority.ARG, Priority.DEFAULT)
            args = FunctionArgInit(priorities=priorities).args
            # CONFIG and ENV are disabled, so should use arg value
            assert args["arg1"] == arg1_value

        fs.create_file("config.yaml", contents=CONFIG)
        env1 = "ARG1"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            test(arg1_value)
