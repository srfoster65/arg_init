"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

from inspect import isclass

import pytest

from arg_init import ArgInit
from arg_init import AttributeExistsError


logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
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
                ArgInit(func_is_bound=True)

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        # Note: arg1 is accessed as _arg1 as protect_attrs=True
        assert test_class._arg1 == arg1_value


    def test_exception_raised_if_protected_attr_exists(self):
        """
        Test exception raised if attempting to set an attribute that already exists
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1=None):
                self._arg1 = "other_value"
                ArgInit(func_is_bound=True)

        with pytest.raises(AttributeExistsError):
            Test()

    def test_exception_raised_if_non_protected_attr_exists(self):
        """
        Test exception raised if attempting to set an attribute that already exists.
        Verify "_" is not used as a prefix to attr when protect_attrs=False.
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1=None):
                self.arg1 = "other_value"
                ArgInit(func_is_bound=True, protect_attrs=False)

        with pytest.raises(AttributeExistsError):
            Test()
