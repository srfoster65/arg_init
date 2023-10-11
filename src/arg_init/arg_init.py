"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""

from inspect import stack, getargvalues
from os import environ
import logging

from box import Box

from .exceptions import AttributeExistsError
from .arg import Arg


logger = logging.getLogger(__name__)


class ArgInit:
    """
    Class to process arguments and environment variables and collate a set of
    processed values.
    """

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY

    def __init__(
        self,
        env_prefix: str = "",
        priority: str = DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
        is_class: bool = False,
        set_attrs: bool = True,  # Only applicable if is_class=True
        args: None | list = None,
    ):
        self._env_prefix = env_prefix
        self._priority = priority
        self._use_kwargs = use_kwargs
        self._is_class = is_class
        self._set_attrs = set_attrs
        self._args = Box()
        self._go(args)

    @property
    def args(self):
        """Return the processed arguments"""
        return self._args

    def _go(self, args: None | list):
        """
        Process args and envs, storing results in self._args
        """
        STACK_LEVEL_OFFSET = 2  # The calling frame is 2 layers up
        calling_stack = stack()[STACK_LEVEL_OFFSET]
        logger.debug("InitArg called for function: %s", calling_stack.function)
        self._process_args(calling_stack.frame, args)
        self._set_class_attrs(calling_stack.frame)
        logger.debug("Finished processing arguments")

    def _process_args(self, frame, args):
        named_args = self._named_arguments(frame)
        for name, value in named_args.items():
            logger.debug("Processing: %s", name)
            arg = self._find_arg(name, args)
            if self._priority == self.ARG_PRIORITY:
                self._arg_priority(arg, value)
            else:
                self._env_priority(arg, value)


    def _named_arguments(self, frame):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and optionally kwargs and their values,
        associated with the specified frame, or the calling function.
        """
        arginfo = getargvalues(frame)
        args = {
            arg: arginfo.locals.get(arg)
            for count, arg in enumerate(arginfo.args)
            if not self._is_class_arg(count)
        }
        if self._use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            args.update(dict(arginfo.locals[keywords].items()) if keywords else {})
        logger.debug("Named arguments: %s", args)
        return args


    def _is_class_arg(self, count: int = 0) -> bool:
        """Return True if the count is 0 and is_class is True"""
        if self._is_class and count == 0:
            logger.debug("Ignoring 1st argument as function is from a class")
            return True
        return False


    @staticmethod
    def _find_arg(name: str, args: None | list) -> str:
        if args:
            logger.debug("Searching for arg=%s", name)
            for arg in args:
                if arg.name == name:
                    logger.debug("Arg found")
                    return arg
            logger.debug("Arg not found")
        else:
            logger.debug("No Args defined")
        logger.debug("Creating arg(name=%s)", name)
        return Arg(name)

    def _arg_priority(self, arg: Arg, value: any) -> None:
        if self._try_arg(arg, value):
            return
        if self._try_env(arg):
            return
        self._try_default(arg)

    def _env_priority(self, arg: Arg, value: any) -> None:
        if self._try_env(arg):
            return
        if self._try_arg(arg, value):
            return
        self._try_default(arg)

    def _try_arg(self, arg: Arg, value: any) -> bool:
        """
        Try and set value from arg
        """
        logger.debug("Checking for an arg")
        if arg.force_arg or value is not None:
            logger.debug("Arg value found: %s", value)
            self._args[self._get_attr_name(arg)] = value
            return True
        logger.debug("Arg value is None and force_arg=False")
        return False

    def _try_env(self, arg: Arg) -> bool:
        """
        Try and set value from env
        """
        env_name = self._get_env_name(arg, self._env_prefix)
        if env_name and env_name in environ and not arg.disable_env:
            logger.debug("Checking for env = '%s'", env_name)
            logger.debug("Found env: %s", env_name)
            value = environ[env_name]
            if arg.force_env or value:
                logger.debug("Env value found: %s", value)
                self._args[self._get_attr_name(arg)] = value
                return True
            logger.debug("env value is None and force_env=False. Checking default")
        else:
            logger.debug("env not found or checking disabled")
        return False

    def _try_default(self, arg: Arg) -> None:
        """
        Try and set value from item default
        """
        logger.debug("Checking for a default value")
        if arg.force_default or arg.default:
            logger.debug("Setting default: %s", arg.default)
            self._args[self._get_attr_name(arg)] = arg.default
        else:
            logger.debug(
                "Not setting %s. Value is None and force_default=False", arg.name
            )

    @staticmethod
    def _get_attr_name(arg: Arg) -> str:
        """Return the name to use for the attribute."""
        return arg.attr if arg.attr else arg.name

    @staticmethod
    def _get_env_name(arg: Arg, prefix: str) -> str:
        """
        Return the env name to check for a value.
        """
        env = arg.env if arg.env else arg.name
        env_parts = [item for item in (prefix, env) if item]
        return "_".join(env_parts).upper()

    def _set_class_attrs(self, frame):
        """Set attributes as defined in "args" for the class object."""
        if self._is_class and self._set_attrs:
            logger.debug("Setting class attributes")
            class_ref = self._get_first_arg(frame)
            for arg, value in self.args.items():
                if hasattr(class_ref, arg):
                    raise AttributeExistsError(arg)
                setattr(class_ref, arg, value)

    def _get_first_arg(self, frame):
        """Return the value of the 1st argument from the calling function."""
        arginfo = getargvalues(frame)
        first_arg = arginfo.args[0]
        return arginfo.locals.get(first_arg)
