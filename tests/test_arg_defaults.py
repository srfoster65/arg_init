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
                alt_name = "ENV1"
                defaults = [ArgDefaults(name=name, alt_name=alt_name)]
                arg_init = ClassArgInit(defaults=defaults)
                assert arg_init.args.arg1.alt_name == alt_name

        Test()
