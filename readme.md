# Overview

[![tests][tests_badge]][tests_url]
[![codecov][codecov_badge]][codecov_url]
[![Docs][docs_badge]][docs_url]
[![PyPI][pypi_badge]][pypi_url]
[![PyPI - License][license_badge]][license_url]

When running code there is often a need to initialise arguments either directly from a passed in value, indirectly via an environment variable or a via default value. Argparse provides this functionality (or can be easily augmented to) already but has one major drawback; It does not work when the code is invoked as a library.

arg_init provides functionality to resolve argument values for a given function/method from either an environment variable, an argument value or a default value. Introspection is used to determine the arguments of the calling function, and a dictionary is created of resolved values for each argument. Resolved values are determined using either Environment Priority (default) or Argument Priority.

When resolving from an environment variable, the environment variable name is assumed to be the same as the argument name, in uppercase e.g. An argument, arg1 would resolve from an environment variable, "ARG1". This behaviour can be modified by providing a custom env_name via argument defaults or by setting an env_prefix.

If the calling function is a class method, arguments may also be made available as class attributes. See reference for more details.

Because it is implemented in the application, it will work if called via a CLI script or as a library by another python program.

**arg_init** provides two classes; ClassArgInit and FunctionArgInit for initialising arguments of bound class functions and unbound functions respectively. These classes iterate over all arguments of the calling function, exposing a dictionary containing key/value pairs of argument name, with values assigned according to the priority system selected.

## Notes

ArgInit uses introspection (via the [inspect](https://docs.python.org/3/library/inspect.html) module) to determine function arguments and values. Its use is minimal and is only executed once at startup so performance should not be an issue.

It is not practical to dynamically determine if the function to be processed is a bound function (a class method, with a class reference (self) as the first parameter) or an unbound function (a simple function), so selection is determined by the use of the called class: ClassArgInit of FunctionArgInit.

Fucntionality is identical for both implementations, with the following exception:

ClassArgInit:

- Class attributes may be set that represent the resolved argument values

If ArgumentParser is used to create a CLI for an application then default values should **not** be assigned in add_argument(). This is to prevent different behaviours between launching as a CLI and an imported library. What happens is that ArgumentParser will provide values for all arguments that have a default assigned. This effectively renders default values in the called function redundant as a value is always provided, even if the value is None.

## Priority

The argument value is set when a non **None** value is found, or all options are exhausted. At this point the argument is set to None.

What priority should be used to set an argument?

### Argument Priority Order

If passed in arguments have priorty over environment variables.

1. Arg
2. Env
3. Default

And if the function has a non **None** default argument e.g. f(a=1), then the argument value will always be used to set the value, never allowing an env value to take effect.

There are two obvious solutions to this:

1. Change the priority order.
2. Provide an alternate means to specify a default value. If a default value is required in the function signature, to allow ommission of an argument when calling, ensure it is set to None.

### Env Priority Order

Environment variables have prioirty over passed in arguments.

1. Env
2. Arg
3. Default

This allows use of the standard default argument values for a python function if no env is defined.

**ArgInit** supports both priority models.
This becomes a personal choice, and behaviour can be chosen at implementation/run time. Default priority order is: **Env Priority**.

## Usage

### Simple Useage

The following examples show how to use arg_init to initialise a class or function, with a default value assigned to the argument.

```python
from arg_init import ClassArgInit

class MyApp:
    def __init__(self, arg1=10):
        ClassArgInit()
        ...
```

```python
from arg_init import FunctionArgInit

def func(arg1=10):
    FunctionArgInit()
    ...
```

In the examples above, arg1 will be initialised with the value from the environment variable "ARG1" if set, else it will take the passed in value. Finally it will have a default value of None assigned.

As these examples use the default priority sytem: ENV_PRIORITY, standard python function defaults can be used in the function signature.

### Other use cases

The example below shows how to change the environment variable name used to initialise the argument using ArgDefaults.

```python
from arg_init import FunctionArgInit, ArgDefaults

def func(arg1=None):
    arg1_defaults = ArgDefaults(env_name="TEST")
    args = FunctionArgInit(defaults={"arg1": arg1_defaults}).args
    ...
```

The example below shows how to use argument priority when resolving the values of arguments.

```python
from arg_init import FunctionArgInit, ARG_PRIOIRITY, ArgDefaults

def func(arg1=None):
    arg1_defaults = ArgDefaults(default_value=1)
    args = FunctionArgInit(priority=ARG_PRIORITY, defaults={"arg1": arg1_defaults}).args
    ...
```

Note:
As this example uses argument priority, a default **must** be provided via ArgDefaults.

### Recommendation

To avoid namespace clashes with environment variables, it is recommneded to always supply an env_prefix argument when initialising ClassArgInit/FunctionArgInit. All environment variables are expected to have this prefix e.g. with an env_prefix of "myapp", arg1 would map to the environment variable "MYAPP_ARG1".

```python
from arg_init import ClassArgInit

class MyApp:
    def __init__(self, arg1=None):
        args = ClassArgInit(env_prefix="myapp").args
        ...
```

Note:
In this example, arg1 would resolve against the environment variable "MYAPP_ARG1".

Please see the [documentation](https://srfoster65.github.io/arg_init/) for further details on usage.

[tests_badge]: https://github.com/srfoster65/arg_init/actions/workflows/build.yml/badge.svg
[tests_url]: https://github.com/srfoster65/arg_init/actions/workflows/build.yml
[codecov_badge]: https://codecov.io/gh/srfoster65/arg_init/graph/badge.svg?token=FFNWSCS4BB
[codecov_url]: https://codecov.io/gh/srfoster65/arg_init
[docs_badge]: https://github.com/srfoster65/arg_init/actions/workflows/docs.yml/badge.svg
[docs_url]: https://srfoster65.github.io/arg_init/
[pypi_badge]: https://img.shields.io/pypi/v/arg-init?logo=python&logoColor=%23cccccc
[pypi_url]: https://pypi.org/project/arg-init
[license_badge]: https://img.shields.io/pypi/l/arg-init
[license_url]: https://srfoster65.github.io/arg-init/license/
