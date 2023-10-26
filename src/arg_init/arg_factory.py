"""
Helper to create Arg objects

Create Arg objects with default values initialised intelligently.
 - "env" will be initialsed as [env_prefix]_[name]
 - "attr" will be initialised as [_][name] if protect_attr is True

Both above conditions are ignored if explicit values are provided for env or attr.
 
"""

from .arg import Arg


class ArgFactory:
    """Factory to assist with creating Arg objects"""

    def __init__(
        self,
        env_prefix: str = "",
        protect_attr: bool = True,  # Only applicable if set_attrs=True
    ):
        self._env_prefix = env_prefix
        self._protect_attr = protect_attr

    def make(
        self,
        name: str,
        env: str = None,
        default: any = None,
        attr: str = None,
        force_arg: bool = False,  # Force use of arg value if value = None
        force_env: bool = False,  # Force use of env value if value = None
        disable_env: bool = False,  # Do not search for an env value
    ):
        """Return an Arg object."""
        return Arg(
            name,
            env=self._get_env_name(name, env),
            default=default,
            attr=self._get_attr_name(name, attr),
            force_arg=force_arg,
            force_env=force_env,
            disable_env=disable_env,
        )

    def _get_env_name(self, name: str, env: str) -> str:
        """Determine the name of the env."""
        if env:
            return env
        env_parts = [item for item in (self._env_prefix, name) if item]
        return "_".join(env_parts).upper()

    def _get_attr_name(self, name, attr):
        """Determine the name of the attr."""
        if attr:
            return attr
        if self._protect_attr:
            return "_" + name if not name.startswith("_") else name
        return name
