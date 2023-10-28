"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

import pytest

from arg_init import ClassArgInit
from arg_init import AttributeExistsError


logger = logging.getLogger(__name__)
Expected = namedtuple('Expected', 'key value')


class TestClassArgInit:
    """
    Test class attributes are initialised
    """

    def test_class(self):
        """
        Test ArgInit on a class method
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1):
                ClassArgInit().resolve()
                assert self._arg1 == arg1_value

        arg1_value = "arg1_value"
        Test(arg1_value)


    def test_exception_raised_if_protected_attr_exists(self):
        """
        Test exception raised if attempting to set an attribute that already exists
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1=None):
                self._arg1 = "other_value"
                ClassArgInit().resolve()

        with pytest.raises(AttributeExistsError):
            Test()

    def test_exception_raised_if_non_protected_attr_exists(self):
        """
        Test exception raised if attempting to set an attribute that already exists.
        Verify "_" is not used as a prefix to attr when protect_args=False.
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1=None):
                self.arg1 = "other_value"
                ClassArgInit().resolve(protect_args=False)

        with pytest.raises(AttributeExistsError):
            Test()
