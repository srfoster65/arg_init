"""
Class to initialise Argument Values for a Function

"""

from inspect import FrameInfo, getargvalues
from typing import Any
import logging

from ._arg_init import ArgInit

logger = logging.getLogger(__name__)


class FunctionArgInit(ArgInit):
    """
    Initialises arguments from a function.
    """

    STACK_LEVEL_OFFSET = 1  # The calling frame is 2 layers up

    def _get_arguments(self, frame: Any, use_kwargs: bool) -> dict:
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        arginfo = getargvalues(frame)
        args = {arg: arginfo.locals.get(arg) for arg in arginfo.args}
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args

    def _get_name(self, calling_stack: FrameInfo) -> str:
        return calling_stack.function
