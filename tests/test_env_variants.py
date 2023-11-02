"""
Test env prefix, env_name and disable_env 
"""

from collections import namedtuple

import pytest

from arg_init import ArgDefaults
from arg_init import FunctionArgInit

Expected = namedtuple('Expected', 'key value')


class TestEnvVariants:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arg_value, envs, defaults, expected",
        [
            ("prefix", None, {"PREFIX_ARG1": "env1_value"}, None, Expected("arg1", "env1_value")),
            ("prefix", None, {"ENV1": "env1_value"}, [ArgDefaults(name="arg1", env_name="ENV1")], Expected("arg1", "env1_value")),
            (None, None, {"ARG1": "env1_value"}, [ArgDefaults(name="arg1", default_value="default", disable_env=True)], Expected("arg1", "default")),
            (None, None, {"ENV1": "env1_value"}, [ArgDefaults(name="arg1", default_value="default", env_name="ENV1", disable_env=True)], Expected("arg1", "default")),
        ],
    )
    def test_env_variants(self, prefix, arg_value, envs, defaults, expected):
        """

        Test advanced env use cases
        1. Prefix - Env is used
        2. Default env_name (Prefix not used) - Env is used
        3. Default env_name with env disabled - Default is used
        4. env_name defined with env_disabled - Default is used

        """
        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(env_prefix=prefix, defaults=defaults).args
            assert args[expected.key] == expected.value

        with pytest.MonkeyPatch.context() as mp:
            if envs:
                for env, value in envs.items():
                    mp.setenv(env, value)
            test(arg1=arg_value)
