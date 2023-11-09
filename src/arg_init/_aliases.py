"""
mypy type aliases
"""

from typing import Any, Optional, Callable

from ._arg_defaults import ArgDefaults
from ._priority import Priority

Defaults = Optional[list[ArgDefaults]]
Priorities= tuple[Priority, Priority, Priority, Priority]
ClassCallback = Callable[[Any], None]
