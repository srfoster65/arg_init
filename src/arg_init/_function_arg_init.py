"""
Class to initialise Argument Values for a Function

"""

from inspect import stack, getargvalues
import logging

from ._arg_init import ArgInit


logger = logging.getLogger(__name__)


class FunctionArgInit(ArgInit):
    """
    Initialises arguments from a function.
    """

    def __init__(self, use_kwargs=False, defaults=None, **kwargs):
        super().__init__(**kwargs)
        if defaults is None:
            defaults = {}
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        self._init_args(calling_stack, use_kwargs, defaults)

    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        arginfo = getargvalues(frame)
        args = {arg: arginfo.locals.get(arg) for arg in arginfo.args}
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args
