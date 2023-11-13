"""Class to represent values used to resolve an argument."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Values:
    """Possible values an argument could be resolved from."""

    arg: Any = None
    env: str | None = None
    config: Any = None
    default: Any = None

    def __repr__(self) -> str:
        return f"<Values(arg={self.arg}, env={self.env}, config={self.config}, default={self.default})>"
