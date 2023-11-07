"""
Test file based argument initialisation
"""

from pathlib import Path

import pytest

from arg_init import FunctionArgInit


class TestFileConfigs:
    """
    """

    def test_toml_file(self, fs):
        """
        Test toml file can be used to initialise arguments
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit().args
            assert args["arg1"] == config1_value

        config1_value = "config1_value"
        config = "[test]\n"\
                 f"arg1='{config1_value}'"
        fs.create_file("config.toml", contents=config)
        test()

    def test_yaml_file(self, fs):
        """
        Test toml file can be used to initialise arguments
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit().args
            assert args["arg1"] == config1_value

        config1_value = "config1_value"
        config = "test:\n"\
                 f"  arg1: {config1_value}"
        fs.create_file("config.yaml", contents=config)
        test()

    def test_json_file(self, fs):
        """
        Test toml file can be used to initialise arguments
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit().args
            assert args["arg1"] == config1_value

        config1_value = "config1_value"
        config = '{"test": {"arg1": "config1_value"}}'
        fs.create_file("config.json", contents=config)
        test()


    def test_named_file_as_string(self, fs):
        """
        Test toml file can be used to initialise arguments
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            args = FunctionArgInit(config_name="named_file").args
            assert args["arg1"] == config1_value

        config1_value = "config1_value"
        config = "[test]\n"\
                 f"arg1='{config1_value}'"
        fs.create_file("named_file.toml", contents=config)
        test()

    def test_specified_file_as_path(self, fs):
        """
        Test toml file can be used to initialise arguments
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            config_name = Path("named_file.toml")
            args = FunctionArgInit(config_name=config_name).args
            assert args["arg1"] == config1_value

        config1_value = "config1_value"
        config = "[test]\n"\
                 f"arg1='{config1_value}'"
        fs.create_file("named_file.toml", contents=config)
        test()

    def test_unsupported_format_raises_exception(self, fs):
        """
        Test unsupported config file format raises an exception
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            config_name = Path("named_file.ini")
            FunctionArgInit(config_name=config_name)

        with pytest.raises(RuntimeError):
            fs.create_file("named_file.ini")
            test()

    def test_missing_named_file_raises_exception(self, fs):
        """
        Test missing named config file raises an exception.
        When an alternate config file is specified, it MUST exist.
        """
        def test(arg1=None):  # pylint: disable=unused-argument
            config_name = Path("missing_file.toml")
            FunctionArgInit(config_name=config_name)

        with pytest.raises(FileNotFoundError):
            test()
