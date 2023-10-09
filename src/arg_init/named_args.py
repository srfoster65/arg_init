"""
Return a list of function parameters from a specified stack frame
"""

from inspect import getargvalues, stack, isclass
import logging


logger = logging.getLogger(__name__)


def named_arguments(frame=None, include_kwargs=False):
    """
    Returns a dictionary containing key value pairs of all
    named arguments and optionally kwargs and their values,
    associated with the specified frame, or the calling function.
    """
    # Select frame of calling function if not set.
    STACK_LEVEL_OFFSET = 1
    frame = frame or stack()[STACK_LEVEL_OFFSET].frame
    arginfo = getargvalues(frame)
    logger.debug(arginfo)
    # get a dictionary of args, ignoring the 1st arg if it is a class type
    # - Assuming this means the frame processed is from a class object
    #   and the 1st argument is self
    args = {
        arg: arginfo.locals.get(arg)
        for count, arg in enumerate(arginfo.args)
        if not _is_class_arg(count, arg)
    }
    if include_kwargs and arginfo.keywords:
        keywords = arginfo.keywords
        logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
        args.update(dict(arginfo.locals[keywords].items()) if keywords else {})
    logger.debug("Named arguments: %s", args)
    return args


def _is_class_arg(count, arg):
    """Return True if the arg is a class type and count is 0."""
    return count == 0 and isclass(arg)
