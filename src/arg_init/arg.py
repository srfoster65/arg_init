"""
Data Class used to customise ArgInit behaviour
"""

from dataclasses import dataclass


@dataclass
class Arg:
    """Class to represent argument attrubutes."""

    name: str  # name of the argument
    env: str = None  # envirnment variable name that contains value.
    default: any = None  # default value if no other source provided a value
    attr: str = None # name of the attribute to apply the value to
    force_arg: bool = False  # Force use of param value if value = None
    force_env: bool = True # Force use of env value if value = None
    force_default: bool = True  # Force use of default value if value = None
    disable_env: bool = False  # Do not search for an env value.
