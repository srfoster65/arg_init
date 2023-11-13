"""
Test env prefix, env_name and disable_env 
"""

from collections import namedtuple

import pytest

from arg_init import FunctionArgInit, ArgDefaults

Expected = namedtuple("Expected", "key value")


class TestEnvVariants:
    """
    Class to test ArgInit for argument priority.
    """

    @pytest.mark.parametrize(
        "prefix, arg_value, envs, defaults, expected",
        [
            ("prefix", None, {"PREFIX_ARG1": "env1_value"}, None, Expected("arg1", "env1_value")),
            (
                "prefix",
                None,
                {"ENV1": "env1_value"},
                [ArgDefaults(name="arg1", alt_name="ENV1")],
                Expected("arg1", "env1_value"),
            ),
        ],
    )
    def test_env_variants(self, prefix, arg_value, envs, defaults, expected, fs):  # pylint: disable=unused-argument
        """

        Test advanced env use cases
        1. Prefix - Env is used
        2. Default env_name (Prefix not used) - Env is used

        """

        def test(arg1):  # pylint: disable=unused-argument
            args = FunctionArgInit(env_prefix=prefix, defaults=defaults).args
            assert args[expected.key] == expected.value

        with pytest.MonkeyPatch.context() as mp:
            if envs:
                for env, value in envs.items():
                    mp.setenv(env, value)
            test(arg1=arg_value)
