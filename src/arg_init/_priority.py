"""Enum to represent priorities supported by arg_init."""

from enum import Enum


class Priority(Enum):
    """Argument resolution priority."""

    CONFIG = 1
    ENV = 2
    ARG = 3
    DEFAULT = 4


# Pre-defined priorities
# The user is free to create and use any priority order using the available options
# defined in Priority
CONFIG_PRIORITY = (Priority.CONFIG, Priority.ENV, Priority.ARG, Priority.DEFAULT)
ENV_PRIORITY = (Priority.ENV, Priority.CONFIG, Priority.ARG, Priority.DEFAULT)
ARG_PRIORITY = (Priority.ARG, Priority.CONFIG, Priority.ENV, Priority.DEFAULT)

DEFAULT_PRIORITY = CONFIG_PRIORITY
