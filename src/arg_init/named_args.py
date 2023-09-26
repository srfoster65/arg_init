"""
Return a list of function parameters from a specified stack frame
"""

from inspect import getargvalues, stack
import logging


FRAME_INDEX = 0
STACK_LEVEL_OFFSET = 1

logger = logging.getLogger(__name__)

def named_arguments(frame=None, include_kwargs=False):
    """
    Returns a dictionary containing key value pairs of all 
    named arguments and optionally kwargs and their values,
    associated with the specified frame, or the calling function.
    """
    # Select frame of calling function if not set.
    frame = frame or stack()[STACK_LEVEL_OFFSET][FRAME_INDEX]
    arginfo = getargvalues(frame)
    logger.debug(arginfo)
    args = {arg: arginfo.locals.get(arg) for arg in arginfo.args if arg != "self"}
    if include_kwargs and arginfo.keywords:
        keywords = arginfo.keywords
        logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
        args.update(dict(arginfo.locals[keywords].items()) if keywords else {})
    logger.debug("Named arguments: %s", args)
    return args
