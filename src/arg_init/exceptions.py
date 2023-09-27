"""
Exceptions raised by package.
"""


class AttributeExistsError(Exception):
    """Exception raised if an attribute already exists."""
    def __init__(self, arg):
        super().__init__(f"Attribute already exists: {arg}")
