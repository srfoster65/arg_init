"""
Dataclass torepresent argument defaults that may be overridden
on a per argument basis.
"""

from dataclasses import dataclass


@dataclass
class ArgDefaults:
    """
    Dataclass to represent argument defaults that may be overridden
    on a per argument basis.
    """

    name: str
    default_value: any = None
    env_name: str = None
    disable_env: bool = False

    def __repr__(self) -> str:
        return (
            f"<ArgDefaults(name={self.name}, "
            f"default_value={self.default_value}, "
            f"env_name={self.env_name}, "
            f"disable_env={self.disable_env})>"
        )
