"""
Class to initialise Argument Values for a Class Method
"""

from inspect import getargvalues
import logging

from ._arg_init import ArgInit
from ._priority import DEFAULT_PRIORITY


logger = logging.getLogger(__name__)


class ClassArgInit(ArgInit):
    """
    Initialises arguments from a class method (Not a simple function).
    The first parameter of the calling function must be a class instance
    i.e. an argument named "self"
    """

    def __init__(
        self,
        priority=DEFAULT_PRIORITY,
        env_prefix=None,
        use_kwargs=False,
        set_attrs=True,
        protect_attrs=True,
        defaults=None,
        config_name="config",
        **kwargs,
    ):
        self._set_attrs = set_attrs
        self._protect_attrs = protect_attrs
        super().__init__(priority, env_prefix, use_kwargs, defaults, config_name, **kwargs)

    def _post_init(self, calling_stack):
        """Class specific post init behaviour."""
        class_instance = self._get_class_instance(calling_stack.frame)
        self._set_class_arg_attrs(class_instance)

    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments for the specified frame. The first
        argument is skipped as this is a reference to the class
        instance.
        """
        arginfo = getargvalues(frame)
        args = {
            arg: arginfo.locals.get(arg)
            for count, arg in enumerate(arginfo.args)
            if count > 0
        }
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args

    def _set_class_arg_attrs(self, class_ref):
        """Set attributes for the class object."""
        if self._set_attrs:
            logger.debug("Setting class attributes")
            for arg in self._args.values():
                self._set_attr(class_ref, arg.name, arg.value)

    def _get_attr_name(self, name):
        if self._protect_attrs:
            return name if name.startswith("_") else "_" + name
        return name

    def _set_attr(self, class_instance, name, value):
        name = self._get_attr_name(name)
        if hasattr(class_instance, name):
            raise AttributeError(f"Attribute already exists: {name}")
        logger.debug("  %s = %s", name, value)
        setattr(class_instance, name, value)

    @staticmethod
    def _get_class_instance(frame):
        """
        Return the value of the 1st argument from the calling function.
        This should be the class instance.
        """
        arginfo = getargvalues(frame)
        first_arg = arginfo.args[0]
        return arginfo.locals.get(first_arg)

    def _get_name(self, calling_stack):
        """Return the name of the current class instance."""
        return calling_stack.frame.f_locals["self"].__class__.__name__
