# Overview

[![Build and Run Unittests](https://github.com/srfoster65/arg_init/actions/workflows/build.yml/badge.svg)](https://github.com/srfoster65/arg_init/actions/workflows/build.yml)
[![build_docs](https://github.com/srfoster65/arg_init/actions/workflows/docs.yml/badge.svg)](https://srfoster65.github.io/arg_init/)
[![codecov](https://codecov.io/gh/srfoster65/arg_init/graph/badge.svg?token=FFNWSCS4BB)](https://codecov.io/gh/srfoster65/arg_init)
[![PyPI](https://img.shields.io/pypi/v/arg-init?logo=python&logoColor=%23cccccc)](https://pypi.org/project/arg-init)

When running code there is often a need to initialise arguments either directly from a passed in value, indirectly via an environment variable or a via default value. Argparse provides this functionality (or can be easily augmented to) already but has one major drawback; It does not work when the code is invoked as a library.

The intention of arg_init is to provide a means, in application code, to initialise function arguments from either an argument, an environment variable or a default value using a well defined priority system. Because it is implemented in the application, it will work if called via a CLI script or as a library by another python program.

If ArgumentParser is used to create a CLI for an application then default values should **not** be assigned in add_argument(). This is to prevent different behaviours between launching as a CLI and an imported library.


**ArgInit** iterates over all arguments of a function, creating a dictionary, containing key/value pairs of argument name, with values assigned according to the priority system selected.

## Notes

arg_init uses introspection (via the [inspect](https://docs.python.org/3/library/inspect.html) module) to determine function arguments and values. Its use is minimal and is only executed once at startup so performance should not be an issue.

Rather than attempt to dynamically determine if the function to be processed is a bound function (a class method, with a class reference (self) as the first parameter) or an unbound function (a simple function), the current implementation requires this be specified at initialisation using the argument **is_class**.

## Priority

The argument value is set when a non **None** value is found.

What priority should be used to set an argument?

### Argument Priority Order

Passed in arguments have prioirty over environment variables.

1. Arg
2. Env
3. Default

But if we use a non **None** default argument value in our function e.g. f(a=1), then the argument value will always be used to set the value, never allowing an env value to take effect.

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

Given a program, implementing a class with a single argument "arg1".

```python
from arg_init import ArgInit

class MyApp:
    def __init__(self, arg1=None):
        ArgInit(is_class=True)
        ...

```

And a CLI script (my_app) to run the program from a shell.

```python
from argparse import ArgumentParser

from my_app import MyApp

parser = ArgumentParser(description="My Application")
parser.add_argument("arg1")
args = parser.parse_args()

app = MyApp(arg1=args.arg1)

```

Calling the CLI script my_app

```script
myapp 42
```

Would result in app.arg1 being assigned the value 42

Calling the CLI script my_app, having first set the environment variable ARG1, as shown below

```script
set ARG1=hello world
myapp
```

Would result in app.arg1 being assigned a value from the environment variable ARG1 of "hello world".

The same program can be launched from another python program, utilising any env configured paramerters. In the example below, arg1 is defined to be 99, but if an env ARG1 were set then arg1 would be initialised with that value.

```python
from my_app import MyApp

a = MyApp(99)

```

### Recommendation

To avoid namespace clashes with environment variables, it is recommneded to always supply an env_prefix argument when initialising ArgInit. ArgInit expects all environment variables to have this prefix e.g. with an env_prefix of "myapp" arg1 would map to the envronment variable "MYAPP_ARG1".

```python
from arg_init import ArgInit

class MyApp:
    def __init__(self, arg1=None):
        ArgInit(env_prefix="myapp", is_class=True)
        ...

```
