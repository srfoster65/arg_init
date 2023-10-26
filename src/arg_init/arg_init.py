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
    Class to process arguments and environment variables and collate a set of
    processed values.
    """

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY
    STACK_LEVEL_OFFSET = 1  # The calling frame is 2 layers up

    def __init__(
        self,
        env_prefix: str = "",
        priority: str = DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
        func_is_bound: bool = False,
        set_attrs: bool = True,  # Only applicable if func_is_bound=True
        protect_attrs: bool = True,  # Only applicable if set_attrs=True
        args: None | list = None,
    ):
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        logger.debug("InitArg called for function: %s", calling_stack.function)
        arg_factory = ArgFactory(env_prefix=env_prefix, protect_attr=protect_attrs)
        function_args = self._function_arguments(
            func_is_bound, calling_stack.frame, use_kwargs
        )
        self._args = self._process_args(function_args, args, arg_factory, priority)
        self._set_class_attrs(func_is_bound, set_attrs, calling_stack.frame)
        logger.debug("Finished processing arguments")

    @property
    def args(self):
        """Return the processed arguments"""
        return self._args

    def _process_args(self, function_args, args, arg_factory, priority):
        _args = Box()
        for name, value in function_args.items():
            arg = self._get_arg(name, args, arg_factory)
            arg.arg.value = value
            arg.resolve(priority)
            _args[arg.name] = arg
        return _args

    def _function_arguments(self, func_is_bound, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and optionally kwargs and their values,
        associated with the specified frame.
        """
        arginfo = getargvalues(frame)
        args = {
            arg: arginfo.locals.get(arg)
            for count, arg in enumerate(arginfo.args)
            if not self._is_self_arg(func_is_bound, count)
        }
        if use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            args.update(dict(arginfo.locals[keywords].items()))
        logger.debug("Named arguments: %s", args)
        return args

    def _is_self_arg(self, func_is_bound, count: int = 0) -> bool:
        """Return True if the count is 0 and func_is_bound is True"""
        if func_is_bound and count == 0:
            logger.debug("Ignoring 1st argument as function is from a class")
            return True
        return False

    def _get_arg(self, name: str, args: None | list, arg_factory: ArgFactory) -> str:
        if args:
            logger.debug("Searching for Arg(name=%s)", name)
            for arg in args:
                if arg.arg.name == name:
                    logger.debug("Arg(%s) found", name)
                    return arg
        logger.debug("Arg(name=%s) not found. Creating default.", name)
        return arg_factory.make(name)

    def _set_attr(self, class_ref, name, value):
        if hasattr(class_ref, name):
            raise AttributeExistsError(name)
        logger.debug("  %s = %s", name, value)
        setattr(class_ref, name, value)

    def _set_class_attrs(self, func_is_bound, set_attrs, frame):
        """Set attributes as defined in "args" for the class object."""
        if func_is_bound and set_attrs:
            logger.debug("Setting class attributes")
            class_ref = self._get_first_arg(frame)
            for arg in self._args.values():
                self._set_attr(class_ref, arg.name, arg.value)

    def _get_first_arg(self, frame):
        """
        Return the value of the 1st argument from the calling function.
        This should be the class instance.
        """
        arginfo = getargvalues(frame)
        first_arg = arginfo.args[0]
        return arginfo.locals.get(first_arg)
