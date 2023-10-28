"""
Helper to create Arg objects

Create Arg objects with default values initialised.
 - "env" will be initialsed as [env_prefix]_[name] if no env value explicitly provided.
 
Both above conditions are ignored if explicit values are provided for env or attr.

"""

import logging

from ._arg import Arg


logger = logging.getLogger(__name__)


#  pylint: disable=too-few-public-methods
class ArgFactory:
    """Factory to assist with creating Arg objects"""

    def __init__(
        self,
        env_prefix: str = "",
    ):
        self._env_prefix = env_prefix

    #  pylint: disable=too-many-arguments
    def make(
        self,
        name: str,
        env: str = None,
        default: any = None,
        force_arg: bool = False,  # Force use of arg value if value = None
        force_env: bool = False,  # Force use of env value if value = None
        disable_env: bool = False,  # Do not search for an env value
    ):
        """Return an Arg object."""
        arg = Arg(
            name,
            env=self._get_env_name(name, env),
            default=default,
            force_arg=force_arg,
            force_env=force_env,
            disable_env=disable_env,
        )
        logger.debug("Created Arg: %s", repr(arg))
        return arg

    def _get_env_name(self, name: str, env: str) -> str:
        """Determine the name to use for the env."""
        if env:
            return env
        env_parts = [item for item in (self._env_prefix, name) if item]
        return "_".join(env_parts).upper()
