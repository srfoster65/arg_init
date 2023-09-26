# process_args

## Installation

With Pip:

```text
pip install arg_init
```

## Overview

When running code there is often a need to initialise arguments either directly from a passed in value, indirectly via an environment variable or a via default value. Argparse provides this functionality (or can be easily augmented to) already but has one major drawback; It does not work when the code is invoked as a library.

The intention of init_params is to provide a means, in application code, to initialise function arguments from either a parameter, environment variable of default value using a well defined priority system. Because it is implemented in the  application, it will work for both use cases.

### Basic Operation

**InitArgs** iterates over all arguments to a function, creating a dictionary, containing key/value pairs of argumnet name/values assigned according to the priority system selected. The key name is referred to as "attribute" in this document to distinguish it fromt he actual argument name. Note: It is possible to map an argument name to a different attribute.

### Priority

The attribute value is set when a non **None** value is found. This behaviour is required to allow working with ArgParse, which will assign a default value of None if no paramter is provided.

What priority should be used to set an attribute?

#### Default Priority Order

1. Arg
2. Env
3. Default

But if we use a non **None** default argument value in our function e.g. f(a=1), then the param value will always be used to set the value, never allowing an env value to take effect.

There are two obvious solutions to this:

1. Change the priority order.
2. Provide an alternate means to specify a default value. If a default value is required in the function signature, to allow ommission of a argument when calling, ensure it is set to None.

#### Alternate Priority Order

1. Env
2. Arg
3. Default

This allows use of the standard default argument values for a python function if no env is defined.

**InitArgss** supports both priority models.
This becomes a personal choice, and behaviour can be chosen at implementation time. This could be user selectable, but most probably hard coded in the application. Default priority order is: arg, env, default.

## Usage

The most simple use case. Given a class with a single argument "arg1".

```python
from arg_init import ArgInit

class MyApp:
    def __init__(self, arg1=None):
        InitArgs().set(self)
        ...

```

Create a CLI script (my_app) to run the program from a shell.

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

Calling the CLI script my_app as shown below

```script
set ARG1=hello world
myapp
```

Would result in app.arg1 being assigned the value "hello world









The same program can be launched from another python program, utilising any env configured paramerters. In the example below, arg1 is defined to be 42, but if this were omitted (or None) then arg1 would be initialised from an environment variable.

```python
from my_app import MyApp

a = MyApp(42)

```
