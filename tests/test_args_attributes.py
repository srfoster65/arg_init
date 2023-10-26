"""
Test ArgItit().args exposes arguments as attributes
"""

from collections import namedtuple
import logging

from arg_init import ArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Test args attributes
    """

    def test_protected_attribute(self):
        """
        Test ArgInit().args exposes arguments as protected attributes
        """
        class Test:
            def __init__(self, arg1):
                self.args = ArgInit().resolve()

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        #  pylint: disable=protected-access
        assert test_class.args._arg1 == arg1_value

    def test_attribute(self):
        """
        Test ArgInit().args exposes arguments as attributes
        """
        class Test:
            def __init__(self, arg1):
                self.args = ArgInit(protect_attrs=False).resolve()

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        assert test_class.args.arg1 == arg1_value
