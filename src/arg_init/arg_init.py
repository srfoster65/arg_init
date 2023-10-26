"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""

from inspect import stack, getargvalues
import logging

from box import Box

from .exceptions import AttributeExistsError
from .arg_factory import ArgFactory


logger = logging.getLogger(__name__)


class ArgInit:
    """
    Class to resolve arguments of a function from passed in values, environment
    variables or default values.
    """

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY
    STACK_LEVEL_OFFSET = 1  # The calling frame is 2 layers up

    def __init__(
        self,
        env_prefix: str = "",
        func_is_bound: bool = False,
        protect_attrs: bool = True,  # Only applicable if set_attrs=True
    ):
        self._func_is_bound = func_is_bound
        self._arg_factory = ArgFactory(
            env_prefix=env_prefix, protect_attr=protect_attrs
        )
        self._args = Box()

    @property
    def args(self):
        """Return the processed arguments."""
        return self._args

    def make_arg(self, name, **kwargs):
        """
        Return an Arg object using the arguments provided
        """
        return self._arg_factory.make(name, **kwargs)

    def resolve(
        self,
        priority: str = DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
        set_attrs: bool = True,  # Only applicable if func_is_bound=True
        args: None | list = None,
    ):
        """
        Resolve argument values
        """
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        logger.debug("Resolving arguments for function: %s", calling_stack.function)
        function_args = self._function_arguments(
            calling_stack.frame, use_kwargs
        )
        for name, value in function_args.items():
            arg = self._get_arg(name, args)
            arg.arg.value = value
            arg.resolve(priority)
            self._args[arg.name] = arg
        self._set_class_attrs(set_attrs, calling_stack.frame)
        return self.args

    def _function_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and optionally kwargs and their values,
        associated with the specified frame.
        """
        arginfo = getargvalues(frame)
        args = {
            arg: arginfo.locals.get(arg)
            for count, arg in enumerate(arginfo.args)
            if not self._is_self_arg(count)
        }
        if use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            args.update(dict(arginfo.locals[keywords].items()))
        logger.debug("Named arguments: %s", args)
        return args

    def _is_self_arg(self, count: int = 0) -> bool:
        """Return True if the count is 0 and func_is_bound is True"""
        if self._func_is_bound and count == 0:
            logger.debug("Ignoring 1st argument as function is from a class")
            return True
        return False

    def _get_arg(self, name: str, args: None | list) -> str:
        if args:
            logger.debug("Searching for Arg(name=%s)", name)
            for arg in args:
                if arg.arg.name == name:
                    logger.debug("Arg(%s) found", name)
                    return arg
        logger.debug("Arg(name=%s) not found. Creating default.", name)
        return self._arg_factory.make(name)

    def _set_class_attrs(self, set_attrs, frame):
        """Set attributes as defined in "args" for the class object."""
        if self._func_is_bound and set_attrs:
            logger.debug("Setting class attributes")
            class_ref = self._get_class_instance(frame)
            for arg in self._args.values():
                self._set_attr(class_ref, arg.name, arg.value)

    def _set_attr(self, class_ref, name, value):
        if hasattr(class_ref, name):
            raise AttributeExistsError(name)
        logger.debug("  %s = %s", name, value)
        setattr(class_ref, name, value)

    def _get_class_instance(self, frame):
        """
        Return the value of the 1st argument from the calling function.
        This should be the class instance.
        """
        arginfo = getargvalues(frame)
        first_arg = arginfo.args[0]
        return arginfo.locals.get(first_arg)
