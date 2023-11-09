"""
Helper module to read a config file

Supported formats are:
- JSON
- TOML
- YAML
"""

from pathlib import Path
from json import load as json_load
from tomllib import load as toml_load
# from typing import Callable, Any, SupportsRead, DefaultNamedArg
from typing import Callable, Any
import logging

from yaml import safe_load as yaml_safe_load


logger = logging.getLogger(__name__)
FORMATS = ["yaml", "toml", "json"]
LoaderCallback = Callable[[Any], dict[Any, Any]]

def _yaml_loader() -> LoaderCallback:
    return yaml_safe_load


def _json_loader() -> LoaderCallback:
    return json_load


def _toml_loader() -> LoaderCallback:
    return toml_load


def _get_loader(path: Path) -> LoaderCallback:
    match path.suffix:
        case ".json":
            return _json_loader()
        case ".yaml":
            return _yaml_loader()
        case ".toml":
            return _toml_loader()
        case _:
            raise RuntimeError(f"Unsupported file format: {path.suffix}")


def _find_config(file: str | Path) -> Path | None:
    if isinstance(file, Path):
        file.resolve()
        logger.debug("Using named config file: %s", file.resolve())
        return file
    for ext in FORMATS:
        path = Path(f"{file}.{ext}").resolve()
        logger.debug("Searching for config: %s", path)
        if path.exists():
            logger.debug("config found: %s", path)
            return path
    logger.debug("No supported config files found")
    return None


def read_config(file: str | Path) -> dict[Any, Any] | None:
    """Read a config file."""
    logger.debug("Reading config file")
    path = _find_config(file)
    if path:
        loader = _get_loader(path)
        with open(path, "rb") as f:
            return loader(f)
    return None
