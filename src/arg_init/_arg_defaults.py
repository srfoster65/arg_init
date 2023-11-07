"""
Dataclass torepresent argument defaults that may be overridden
on a per argument basis.
"""

from dataclasses import dataclass
from typing import Any

@dataclass
class ArgDefaults:
    """
    Dataclass to represent argument defaults that may be overridden
    on a per argument basis.
    """

    name: str
    default_value: Any = None
    alt_name: str | None = None

    def __repr__(self) -> str:
        return (
            f"<ArgDefaults(name={self.name}, "
            f"default_value={self.default_value}, "
            f"alt_name={self.alt_name})>"
        )
