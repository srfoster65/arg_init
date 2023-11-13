"""Exceptions raised by arg-init."""

from typing import Any


class UnsupportedFileFormatError(Exception):
    def __init__(self, suffix: str, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        msg = f"Unsupported file format: {suffix}"
        super().__init__(msg, *args, **kwargs)
