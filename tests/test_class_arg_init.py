"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple

import pytest

from arg_init import ClassArgInit


Expected = namedtuple("Expected", "key value")


class TestClassArgInit:
    """
    Test class attributes are initialised
    """

    def test_class(self, fs):  # pylint: disable=unused-argument
        """
        Test ArgInit on a class method
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1):  # pylint: disable=unused-argument
                ClassArgInit()
                assert self._arg1 == arg1_value  # pylint: disable=no-member

        arg1_value = "arg1_value"
        Test(arg1_value)

    def test_protect_attr_false_sets_attr(self, fs):  # pylint: disable=unused-argument
        """
        Test ArgInit on a class method
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1):  # pylint: disable=unused-argument
                ClassArgInit(protect_attrs=False)
                assert self.arg1 == arg1_value  # pylint: disable=no-member

        arg1_value = "arg1_value"
        Test(arg1_value)

    def test_exception_raised_if_protected_attr_exists(self, fs):  # pylint: disable=unused-argument
        """
        Test exception raised if attempting to set an attribute that already exists
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):  # pylint: disable=unused-argument
                self._arg1 = "other_value"
                ClassArgInit()

        with pytest.raises(AttributeError):
            Test()

    def test_exception_raised_if_non_protected_attr_exists(self, fs):  # pylint: disable=unused-argument
        """
        Test exception raised if attempting to set an attribute that already exists.
        Verify "_" is not used as a prefix to attr when protect_args=False.
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):  # pylint: disable=unused-argument
                self.arg1 = "other_value"
                ClassArgInit(protect_attrs=False)

        with pytest.raises(AttributeError):
            Test()

    def test_set_attrs_false_does_not_set_attrs(self, fs):  # pylint: disable=unused-argument
        """
        Test exception raised if attempting to set an attribute that already exists.
        Verify "_" is not used as a prefix to attr when protect_args=False.
        """

        class Test:
            """Test Class"""

            def __init__(self, arg1=None):  # pylint: disable=unused-argument
                self.arg1 = "other_value"
                ClassArgInit(set_attrs=False)
                assert hasattr(self, "_arg1") is False

        Test()
