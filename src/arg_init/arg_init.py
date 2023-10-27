"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""
from abc import ABC, abstractmethod
# from inspect import stack, getargvalues
import logging

from box import Box

# from .exceptions import AttributeExistsError
from .arg_factory import ArgFactory


logger = logging.getLogger(__name__)



ARG_PRIORITY = "arg_priority"
ENV_PRIORITY = "env_priority"


class ArgInit(ABC):
    """
    Class to resolve arguments of a function from passed in values, environment
    variables or default values.
    """

    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY
    STACK_LEVEL_OFFSET = 1  # The calling frame is 1 layer up

    def __init__(
        self,
        env_prefix: str = "",
    ):
        self._arg_factory = ArgFactory(
            env_prefix=env_prefix
        )
        self._args = Box()

    @property
    def args(self) -> Box:
        """Return the processed arguments."""
        return self._args

    @abstractmethod
    def resolve(self, priority, use_kwargs, set_attrs, protect_attrs):
        """Virtual function to be implemented by any derived class."""
        raise RuntimeError("_get_arguments() must be implement in derived class")  # pragma no cover


    @abstractmethod
    def _get_arguments(self, frame, use_kwargs):
        """Virtual function to be implemented by any derived class."""
        raise RuntimeError("_get_arguments() must be implement in derived class")  # pragma no cover

    def make_arg(self, name, **kwargs):
        """
        Create an Arg object using the arguments provided.
        Retruns the key the Arg is stored under in self._args.
        """
        arg = self._arg_factory.make(name, **kwargs)
        self._args[name] = arg

    def _resolve(
        self,
        calling_stack,
        priority: str = DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
    ) -> None:
        """
        Resolve argument values
        """
        logger.debug("Resolving arguments for function: %s", calling_stack.function)
        arguments = self._get_arguments(calling_stack.frame, use_kwargs)
        self._make_args(arguments)
        self._resolve_args(priority)

    def _get_kwargs(self, arginfo, use_kwargs) -> dict:
        """
        Return a dictionary containing kwargs to be resolved.
        Returns an empty dictionary if use_kwargs=False
        """
        if use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            return dict(arginfo.locals[keywords].items())
        return {}

    def _make_args(self, arguments) -> None:
        for name, value in arguments.items():
            self._make_arg(name)
            self._args[name].arg.value = value

    def _resolve_args(self, priority) -> None:
        for arg in self._args.values():
            arg.resolve(priority)

    def _make_arg(self, name: str) -> None:
        """
        Make default Arg if one does not already exist in self._args
        """
        logger.debug("Searching for Arg(name=%s)", name)
        if name not in self._args:
            logger.debug("Arg(name=%s) not found. Creating default.", name)
            self.make_arg(name)
