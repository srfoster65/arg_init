"""mypy type aliases."""

from collections.abc import Callable
from typing import Any

from ._arg_defaults import ArgDefaults
from ._priority import Priority

ClassCallback = Callable[[Any], None]
Defaults = list[ArgDefaults] | None
LoaderCallback = Callable[[Any], dict[Any, Any]]
Priorities = tuple[Priority, Priority, Priority, Priority]
