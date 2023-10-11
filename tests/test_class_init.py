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
            """
            blah
            """
            def __init__(self, arg1):
                ArgInit(is_class=True)

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)

        print('in pytest', isclass(test_class))

        assert test_class.arg1 == arg1_value


    def test_attribute_exists_not_set(self):
        """
        Test exception raised if attempting to set an attribute that already exists
        """
        class Test:
            def __init__(self, arg1):
                self.arg1 = "other_value"
                ArgInit(is_class=True)

        with pytest.raises(AttributeExistsError):
            arg1_value = "arg1_value"
            Test(arg1_value)

    def test_attribute_not_set(self):
        """
        Test exception raised if attempting to set an attribute that already exists
        """
        class Test:
            def __init__(self, arg1):
                ArgInit(is_class=True, set_attrs=False)

        with pytest.raises(AttributeError):
            arg1_value = "arg1_value"
            arg1  = Test(arg1=arg1_value).args["arg1"]

