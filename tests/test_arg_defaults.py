"""
Test ArgDefaults
"""

import logging

from arg_init import ClassArgInit, ArgDefaults

logger = logging.getLogger(__name__)


class TestArgDefaults:
    """
    Test default values are correctly applied when creating args
    """

    def test_default_value(self):
        """
        Test overriding default_value
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):
                name = "arg1"
                default_value = "arg1_default"
                defaults = [ArgDefaults(name=name, default_value=default_value)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.values.default == default_value

        Test()

    def test_env_name(self):
        """
        Test overriding env_name
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):
                name = "arg1"
                env_name = "ENV1"
                defaults = [ArgDefaults(name=name, env_name=env_name)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.env_name == env_name

        Test()

    def test_disable_env(self):
        """
        Test disable_env=True sets env_name to None
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):
                name = "arg1"
                env_name = "ENV1"
                disable_env = True
                defaults = [ArgDefaults(name=name, env_name=env_name, disable_env=disable_env)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.env_name is None

        Test()
