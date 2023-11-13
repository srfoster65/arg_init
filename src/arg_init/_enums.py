"""Enums used by arg_init."""

from enum import Enum


class UseKWArgs(Enum):
    # Use 0 as 1st enum to allow simple boolean eqivalence test
    FALSE = False
    TRUE = True


class SetAttrs(Enum):
    # Use 0 as 1st enum to allow simple boolean eqivalence test
    FALSE = False
    TRUE = True


class ProtectAttrs(Enum):
    # Use 0 as 1st enum to allow simple boolean eqivalence test
    FALSE = False
    TRUE = True
