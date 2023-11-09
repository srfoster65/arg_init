"""
Class to initialise Argument Values for a Class Method
"""

from inspect import getargvalues, FrameInfo
from pathlib import Path
from typing import Any, Optional, Callable
import logging

from ._aliases import Defaults, Priorities, ClassCallback
from ._arg_init import ArgInit
from ._priority import DEFAULT_PRIORITY


logger = logging.getLogger(__name__)


class ClassArgInit(ArgInit):
    """
    Initialises arguments from a class method (Not a simple function).
    The first parameter of the calling function must be a class instance
    i.e. an argument named "self"
    """

    STACK_LEVEL_OFFSET = 2  # The calling frame is 2 layers up

    def __init__(
        self,
        priorities: Priorities = DEFAULT_PRIORITY,
        env_prefix: Optional[str] = None,
        use_kwargs: bool = False,
        defaults: Defaults = None,
        config_name: str | Path = "config",
        set_attrs: bool = True,
        protect_attrs: bool = True,
        **kwargs: dict[Any, Any],  # pylint: disable=unused-argument
    ) -> None:
        self._set_attrs = set_attrs
        self._protect_attrs = protect_attrs
        super().__init__(priorities, env_prefix, use_kwargs, defaults, config_name, **kwargs)

    def _post_init(self, calling_stack: FrameInfo) -> None:
        """Class specific post init behaviour."""
        class_instance = self._get_class_instance(calling_stack.frame)
        self._set_class_arg_attrs(class_instance)

    def _get_arguments(self, frame: Any, use_kwargs: bool) -> dict[Any, Any]:
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

    def _set_class_arg_attrs(self, class_ref: ClassCallback) -> None:
        """Set attributes for the class object."""
        if self._set_attrs:
            logger.debug("Setting class attributes")
            for arg in self._args.values():
                self._set_attr(class_ref, arg.name, arg.value)

    def _get_attr_name(self, name: str) -> str:
        if self._protect_attrs:
            return name if name.startswith("_") else "_" + name
        return name

    def _set_attr(self, class_instance: ClassCallback, name: str, value: Any) -> None:
        name = self._get_attr_name(name)
        if hasattr(class_instance, name):
            raise AttributeError(f"Attribute already exists: {name}")
        logger.debug("  %s = %s", name, value)
        setattr(class_instance, name, value)

    @staticmethod
    def _get_class_instance(frame: Any) -> ClassCallback:
        """
        Return the value of the 1st argument from the calling function.
        This should be the class instance.
        """
        arginfo = getargvalues(frame)
        first_arg = arginfo.args[0]
        return arginfo.locals[first_arg]

    def _get_name(self, calling_stack: FrameInfo) -> str:
        """Return the name of the current class instance."""
        return calling_stack.frame.f_locals["self"].__class__.__name__
