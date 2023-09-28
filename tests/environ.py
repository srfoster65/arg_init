"""
Decorator to patch an environment variable.
"""

import contextlib
import os
from functools import wraps


# def patch_environ(new_environ=None, clear_orig=False):
#     """
#     Decorator to patch an environment variable.

#     Usage:
#     @patch_environ({"new_env": "test value"})
#     def test()
#         assert os.environ["new_env"] == "test_value"

#     """
#     if not new_environ:
#         new_environ = dict()

#     def wrapper_patch_environ(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             original_env = dict(os.environ)

#             if clear_orig:
#                 os.environ.clear()

#             os.environ.update(new_environ)
#             try:
#                 result = func(*args, **kwargs)
#             # except:
#             #     raise
#             finally:  # restore even if Exception was raised
#                 os.environ = original_env

#             return result

#         return wrapper

#     return wrapper_patch_environ


@contextlib.contextmanager
def modified_environ(*remove, **update):
    """
    Temporarily updates the ``os.environ`` dictionary in-place.

    The ``os.environ`` dictionary is updated in-place so that the modification
    is sure to work in all situations.

    :param remove: Environment variables to remove.
    :param update: Dictionary of environment variables and values to add/update.
    """
    env = os.environ
    update = update or {}
    remove = remove or []

    # List of environment variables being updated or removed.
    modified = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in modified}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update({key: str(value) for key, value in update.items()})
        [env.pop(k, None) for k in remove]
        yield
    finally:
        # Restore environ back to starting configuration
        env.update(update_after)
        [env.pop(k) for k in remove_after]
