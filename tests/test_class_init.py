"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

import pytest

from arg_init import Arg
from arg_init import ArgInit

from .environ import modified_environ


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Test class attributes are initialised
    """

    def test_init(self):
        """
        Test ArgInit.set sets attributes of class
        """
        class Test:
            def __init__(self, arg1):
                ArgInit().set(self)

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        assert test_class.arg1 == arg1_value
