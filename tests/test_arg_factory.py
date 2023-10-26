"""
Test ArgInit class variable initialisation.
"""

from collections import namedtuple
import logging

from inspect import isclass

import pytest

from arg_init import ArgInit
# from arg_init import AttributeExistsError
from arg_init import ArgFactory

logger = logging.getLogger(__name__)
Expected = namedtuple('Expcted', 'key value')


class TestDefaultConfig:
    """
    Test class attributes are initialised
    """

    def test_single_arg(self):
        """
        Test ArgInit on a class method
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1):
                arg_init = ArgInit(func_is_bound=True)
                args = [arg_init.make_arg(name=arg1)]
                arg_init.resolve(args=args)

        arg1 = "arg1"
        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        # Note: arg1 is accessed as _arg1 as protect_attrs=True
        assert test_class._arg1 == arg1_value

    def test_env_prefix_arg(self):
        """
        Test factory created arg sets env prefix
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1):
                arg_init = ArgInit(func_is_bound=True, env_prefix="prefix")
                args = [arg_init.make_arg(name=arg1)]
                arg_init.resolve(args=args)

        env1 = "PREFIX_ARG1"
        env1_value = "env1_value"
        arg1_value = "arg1_value"
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv(env1, env1_value)
            test_class = Test(arg1_value)
            # Note: arg1 is accessed as _arg1 as protect_attrs=True (default)
            assert test_class._arg1 == env1_value

    def test_protect_false_arg(self):
        """
        Test factory created Arg sets attr value correctly
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1):
                arg_init = ArgInit(func_is_bound=True, protect_attrs=False)
                args = [arg_init.make_arg(arg1)]
                arg_init.resolve(args=args)

        arg1_value = "arg1_value"
        test_class = Test(arg1_value)
        # Note: arg1 is accessed as _arg1 as protect_attrs=True (default)
        assert test_class.arg1 == arg1_value

    def test_multiple_args(self):
        """
        Test ArgInit on a class method
        """
        class Test:
            """Test Class"""
            def __init__(self, arg1, arg2):
                arg_init = ArgInit(func_is_bound=True)
                args = [arg_init.make_arg(arg1), arg_init.make_arg(arg2)]
                arg_init.resolve(args=args)

        arg1_value = "arg1_value"
        arg2_value = "arg2_value"
        test_class = Test(arg1_value, arg2_value)
        # Note: arg1 is accessed as _arg1 as protect_attrs=True (default)
        assert test_class._arg1 == arg1_value
        assert test_class._arg2 == arg2_value

