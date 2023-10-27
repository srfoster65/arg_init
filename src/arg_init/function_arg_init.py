"""

"""


from inspect import stack, getargvalues
import logging

from .arg_init import ArgInit


logger = logging.getLogger(__name__)


class FunctionArgInit(ArgInit):
    """
    Initialises arguments from a function.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def resolve(
        self,
        priority: str = ArgInit.DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
    ):
        """
        Resolve argument values
        """
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        self._resolve(calling_stack, priority, use_kwargs)
        return self._args

    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame,
        skipping the first argument as this is a reference to the
        class instance.
        """
        arginfo = getargvalues(frame)
        args = {arg: arginfo.locals.get(arg) for count, arg in enumerate(arginfo.args)}
        args.update(self._get_kwargs(arginfo, use_kwargs))
        return args
