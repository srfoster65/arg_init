# Overview

[![tests][tests_badge]][tests_url]
[![codecov][codecov_badge]][codecov_url]
[![mypy][mypy_badge]][mypy_url]
[![Ruff][ruff_badge]][ruff_url]
[![Docs][docs_badge]][docs_url]
[![PyPI][pypi_badge]][pypi_url]
[![PyPI - License][license_badge]][license_url]

When running code there is often a need to initialise arguments either directly from a passed in value, indirectly via an environment variable or config file or a via default value. Argparse provides this functionality (or can be easily augmented to, with the exception of loading from a config file) already but has one major drawback; It does not work when the code is invoked as a library.

arg_init provides functionality to resolve argument values for a given function/method from either a config file, an environment variable, an argument value or a default value. Introspection is used to determine the arguments of the calling function, and a dictionary is created of resolved values for each argument. Resolved values are determined using a predefined priority system that can be customised by the user.

When resolving from an environment variable, the environment variable name is assumed to be the same as the argument name, in uppercase e.g. An argument, arg1 would resolve from an environment variable, "ARG1". This behaviour can be modified by providing an alternate name via argument defaults or by setting an env_prefix.

If the calling function is a class method, arguments may also be made available as class attributes. See reference for more details.

Because argument initialisation is implemented in the application, it will work if called via a CLI script or as a library by another python program.

**arg_init** provides two classes; ClassArgInit and FunctionArgInit for initialising arguments of bound class functions and unbound functions respectively. These classes iterate over all arguments of the calling function, exposing a dictionary containing key/value pairs of argument name, with values assigned according to the priority system selected.

## Notes

arg_init uses introspection (via the [inspect](https://docs.python.org/3/library/inspect.html) module) to determine function arguments and values. Its use is minimal and is only executed once at startup so performance should not be an issue.

It is not practical to dynamically determine if the function to be processed is a bound function (a class method, with a class reference (self) as the first parameter) or an unbound function (a simple function), so selection is determined by the use of the called class: ClassArgInit of FunctionArgInit.

Fucntionality is identical for both implementations, with the following exception:

ClassArgInit:

- Class attributes are set (may be optionally disabled) that represent the resolved argument values

## Priority

The argument value is set when a non **None** value is found, or all options are exhausted. At this point the argument is set to None.

What priority should be used to set an argument?

### Argument Priority Order

If passed in arguments have priorty:

And if the function has a non **None** default argument e.g. f(a=1), then the argument value will always be used to set the value, never allowing a config or env value to take effect.

There are two obvious solutions to this:

1. Lower the priority of arguments.
2. Provide an alternate means to specify a default value. If a default value is required in the function signature, to allow ommission of an argument when calling, ensure it is set to None.

### Default Values

The problem: How to avoid violating the DRY principle when an application can be invoked via a CLI or as a library.

If an application is to be called as a library then the defaults MUST be implemented in the application, not the CLI script. But ArgumentParser will pass in None values if no value is specified for an argument. This None value will be used in preference to function default! So defaults must be also be specified in ArgumentParser and the applicication. This is not a good design pattern.

Providing an alternate means to specify a default value resolves this.

### Priority Order

**arg-init** supports customisable priority models.
It is left to the user to select an appropriate priority sequence (or use the default option) for each specfic use case.

#### Default Priority Order

The default priority implemented is:

**CONFIG_PRIORITY**

  1. Config
  2. Env
  3. Arg
  4. Default

#### Predefined Priority Orders

Two further predifined priority models are provided

- **ENV_PRIORITY**
- **ARG_PRIOIRTY**

The user may also define a custom priority order if the predefined options are not suitable.

## Usage

### Simple Useage

The following examples show how to use arg_init to initialise a class or function

```python
from arg_init import ClassArgInit

class MyApp:
    def __init__(self, arg1=None):
        ClassArgInit()
        ...
```

```python
from arg_init import FunctionArgInit

def func(arg1=None):
    FunctionArgInit()
    ...
```

In the examples above, arg1 will be initialised with the value from the config file, the environment variable "ARG1", else it will take the passed in value. Finally it will have a default value of None assigned.

As these examples use the default priority sytem, they will not work if used with ArgumentParser without ArgumentParser replicating the default values.

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
    arg1_defaults = ArgDefaults("arg1", default_value=1)
    args = FunctionArgInit(priority=ARG_PRIORITY, defaults=[arg1_defaults]).args
    ...
```

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
[mypy_badge]: https://github.com/srfoster65/arg_init/actions/workflows/mypy.yml/badge.svg
[mypy_url]: https://github.com/srfoster65/arg_init/actions/workflows/mypy.yml
[ruff_badge]: https://github.com/srfoster65/arg_init/actions/workflows/lint.yml/badge.svg
[ruff_url]: https://github.com/srfoster65/arg_init/actions/workflows/lint.yml
[docs_badge]: https://github.com/srfoster65/arg_init/actions/workflows/docs.yml/badge.svg
[docs_url]: https://srfoster65.github.io/arg_init/
[pypi_badge]: https://img.shields.io/pypi/v/arg-init?logo=python&logoColor=%23cccccc
[pypi_url]: https://pypi.org/project/arg-init
[license_badge]: https://img.shields.io/pypi/l/arg-init
[license_url]: https://srfoster65.github.io/arg-init/license/
