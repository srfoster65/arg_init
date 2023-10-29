"""
Test ArgInit class variable initialisation.
"""

import logging

from arg_init import ClassArgInit, ArgDefaults

logger = logging.getLogger(__name__)


class TestUpdateArg:
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
                default_value = "arg1_default"
                defaults = {"arg1": ArgDefaults(default_value=default_value)}
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
                env_name = "ENV1"
                defaults = {"arg1": ArgDefaults(env_name=env_name)}
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.env_name == env_name

        Test()

    def test_disable_env(self):
        """
        Test overriding disable_env
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):
                env_name = "ENV1"
                disable_env = True
                defaults = {
                    "arg1": ArgDefaults(env_name=env_name, disable_env=disable_env)
                }
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.env_name is None

        Test()
