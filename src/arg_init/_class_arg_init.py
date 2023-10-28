"""
Class to initialise Argument Values for a Class Method
"""

from inspect import stack, getargvalues
import logging

from ._arg_init import ArgInit
from ._exceptions import AttributeExistsError


logger = logging.getLogger(__name__)


class ClassArgInit(ArgInit):
    """
    Initialises arguments from a class method (Not a simple function).
    The first parameter of the calling function must be a class instance
    i.e. an argument named "self"
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def resolve(
        self,
        priority: str = ArgInit.DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
        set_attrs: bool = True,
        protect_args: bool = True,
        **kwargs
    ):
        """Resolve argument values."""
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        self._resolve(calling_stack, priority, use_kwargs)
        self._set_class_attrs(set_attrs, protect_args, calling_stack.frame)
        return self._args

    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame,
        skipping the first argument as this is a reference to the
        class instance.
        """
        arginfo = getargvalues(frame)
        args = {
            arg: arginfo.locals.get(arg)
            for count, arg in enumerate(arginfo.args)
            if count > 0
        }
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args

    def _set_class_attrs(self, set_attrs, protect_args, frame):
        """Set attributes as defined in "args" for the class object."""
        if set_attrs:
            logger.debug("Setting class attributes")
            class_ref = self._get_class_instance(frame)
            for arg in self._args.values():
                arg_name = self._get_arg_name(arg.name, protect_args)
                self._set_attr(class_ref, arg_name, arg.value)

    @staticmethod
    def _get_arg_name(name, protect_arg):
        if protect_arg:
            return name if name.startswith("_") else "_" + name
        return name

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
