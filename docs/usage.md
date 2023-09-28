# Usage

## Installation

With Pip:

```text
pip install arg_init
```

## Basic Usage

ArgInit should be called from a function or class \_\_init\_\_() method that arguments should be processed for. ArgInit will determine the arguments of the calling function and resolve a value for each argument in turn from either an environment variable, the argument value or a default value.

All environment variables must begin with the prefix MYAPP_ to ensure there are no namespace clashes.

```python
from arg_init import ArgInit

def my_func(arg1=99):
    args = ArgInit(env_prefix="MYAPP").args

my_func(101)

```

Running the above program with a clean environment would result in:

1. With a clean environment:
        args.arg1 = 101
2. With the envirnment variable MYAPP_ARG1 set to "1":
        args.arg1 = 1
3. With the program modified to call my_func():
        args.arg1 = 99

### Overriding Default Argument Behaviour

It is possible to override default behaviour per argument by providing a list of Arg objects at initialisation time.

```python
from arg_init import ArgInit, Arg

def my_func(arg1):
    arg_1 = Arg("arg1", force_arg=True)
    args = ArgInit(env_prefix="MYAPP", args=[arg_1]).args
    ...
```

In this instance, no default is supplied for arg1 in the function definition as a value of **None** will be assigned in the absence of any env or argument being supplied.

## Use with a Class

When used with a class ArgInit is expected to be called from the \_\_init\_\_() method. It also expects teh first parameter to be a class instance "self" and so ignores this argument. All other arguments are processed.

```python
from arg_init import ArgInit

class MyApp:
    def __init__(self, arg1=None):
        ArgInit(env_prefix="myapp").set(self)
        ...

```

The call to set() passing in the argument "self", will set attributes with the same name as the arguments on the MyApp class instance.

### Modifying Class Attributes Names

The names of the resolved arguments, and hence applied class attributes can be modified with the use of the Arg object and the attr argument.

```python
from arg_init import ArgInit, Arg

class MyApp:
    def __init__(self, arg1=None):
        arg_1 = Arg("arg1", attr="_arg1")
        ArgInit(env_prefix="myapp", args=[arg_1]).set(self)
        ...

```

In the example above, the instance of MyApp would have an attribute **_arg1** set with a value provided by resolving the arg1 argument.

## Support for kwargs

Support for kwargs in function signatures is provided via the argument **use_kwargs**.


```python
from arg_init import ArgInit, Arg

def my_func(self, **kwargs):
    args = ArgInit(env_prefix="myapp", use_kwargs=True).args
    ...

fn = my_func({"test": "hello"})

```

Running the above program would result in fn.args.test being assigned the value "hello"

As before, environment variables will also be processed. If an envirnment variable MYAPP_TEST were assigned the value of "world", this would result in fn.args.test being assigned the value "world".
