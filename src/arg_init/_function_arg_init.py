"""
Class to initialise Argument Values for a Function

"""

from inspect import getargvalues
import logging

from ._arg_init import ArgInit
from ._priority import DEFAULT_PRIORITY

logger = logging.getLogger(__name__)


class FunctionArgInit(ArgInit):
    """
    Initialises arguments from a function.
    """

    def __init__(
        self,
        priority=DEFAULT_PRIORITY,
        env_prefix=None,
        use_kwargs=False,
        defaults=None,
        config_name="config",
        **kwargs,
    ):
        super().__init__(priority, env_prefix, use_kwargs, defaults, config_name, **kwargs)

    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        arginfo = getargvalues(frame)
        args = {arg: arginfo.locals.get(arg) for arg in arginfo.args}
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args

    def _get_name(self, calling_stack):
        return calling_stack.function
