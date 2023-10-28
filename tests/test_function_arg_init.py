"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

from arg_init import FunctionArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestFunctionArgInit:
    """
    Test class attributes are initialised
    """

    def test_class(self):
        """
        Test ArgInit on a class method
        """
        def test(arg1):
            """Test Class"""
            args = FunctionArgInit().resolve()
            assert args.arg1 == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
