"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

import pytest

from arg_init import FunctionArgInit


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestFunctionArgInitConfig:
    """
    Test class attributes are initialised
    """

    def test_class(self):
        """
        Test ArgInit on a class method
        """
        def test(arg1):
            """Test Class"""
            def __init__(self, arg1):
                FunctionArgInit().resolve()
                assert self.args.arg1 == arg1_value

        arg1_value = "arg1_value"
        test(arg1_value)
