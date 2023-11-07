"""
Test _version.py contains a version.
"""

from arg_init._version import __version__


class TestVersionDefined:
    """
    Test a version is defined in _version.py
    """

    def test_version_defined(self):
        """
        Test kwargs are ignored if not explicity enabled
        """
        assert __version__
