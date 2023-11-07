# Usage

## Installation

With Pip:

```text
pip install arg_init
```

## Basic Usage for Class functions

For Class methods: ClassArgInit() should be called from a class \_\_init\_\_() method that arguments should be processed for.

```python
from arg_init import ClassArgInit

class MyClass:
    def __init__(self, arg1=99):
        ClassArgInit().args
        print(self._arg1)
```

Resolved arguments are exposed as protected class attributes e.g. "self._arg1".

## Basic Usage for simple functions

FunctionArgInit() should be called from a function that arguments should be processed for.

```python
from arg_init import FunctionArgInit

def my_func(arg1=None):
    args = FunctionArgInit().args
    print(args.arg1)
```

Resolved arguments are exposed by accessing the args attribute of FunctionArgInit. Resolved values can be accessed as attributes e.g. args.arg1 or as a dictionary item e.g. args["arg1"].

## Other Use Cases

### Using config files to resolve argument values

By default arg-init will search for a config file named "config", with the extension: toml, yaml, json (in that order) in the current working directory. This behaviour can be overridden by specifying an absolute or relative path to a different config file.

#### TOML files

The section heading should be the name of the class, if using ClassArgInit or the name of the function, if using FunctionArgInit.

```toml
[MyApp]
arg1 = 42
```

#### YAML Files

The top level dictionary key should be the name of the class, if using ClassArgInit or the name of the function, if using FunctionArgInit.

```yaml
MyApp:
  arg1: 42
```

#### JSON Files

The top level dictionary key should be the name of the class, if using ClassArgInit or the name of the function, if using FunctionArgInit.

```json
{
  "MyApp":
  {
    "arg1": 42
  }
}
```

### Setting a Common Prefix for all Environment Variables

To avoid namespace clashes with environment variables, it is recommneded to always supply an env_prefix argument when initialising ClassArgInit/FunctionArgInit. All environment variables are expected to have this prefix e.g. with an env_prefix of "myapp", arg1 would map to the environment variable "MYAPP_ARG1".

```text
env_prefix=<string>
```

env_prefix is converted to uppercase before use.

```python
from arg_init import ClassArgInit

class MyApp:
    def __init__(self, arg1=None):
        args = ClassArgInit(env_prefix="myapp").args
        ...
```

### Priority Modes

Support for selecting the priority resolution mode is provided via the argument **priority**.

```text
priority=ENV_PRIORITY | ARG_PRIORITY
```

By default, enviroment variables have priority over argument values. This can be changed at initialisation to give arguments prioirty.

```python
from arg_init import FunctionArgInit, ARG_PRIORITY

def my_func(arg1):
    arg_init = FunctionArgInit()
    args = arg_init.resolve(priority=ARG_PRIORITY)
    ...
```

Note: When using ARG_PRIORITY a default value should also be provided by ArgDefaults is a default value other than None is required.

### Overriding Default Argument Behaviour

It is possible to override default behaviour per argument using the ArgDefault object. A list of ArgDefaults objects can be passed into the call to ClassArgInit/FunctionArgInit.

ArgDefaults takes a "name" argumment and zero or more of the following optional arguments:

+ default_value
+ env_name

#### default_value

When using ARG_Priority, the only way to set a default value is to the use ArgDefaults(default_value=value)

This can also be used when using ENV_Priority but the recommended solution is to use default python behaviour using function defaults e.g. fn(a=1).

#### env_name

Setting this value allows a custom env name to be set as the lookup for an argument. This overrides the default setting and ignores any env prefix settings.

Note: env_name is converted to uppercase before use.

#### Example using ArgDefaults

In the example below, arg1 is modified to have a default value of 1 and to resolve from the environmnet variable "ALT_NAME"

```python
from arg_init import FunctionArgInit, ArgDefaults

def func(arg1=None):
    arg1_defaults = ArgDefaults(name="arg1", default_value=1, env_name="ALT_NAME")
    args = FunctionArgInit(defaults=[arg1_defaults]).args
    ...
```

### Use with a Class

There are two additional class specific configuration options available:

+ set_attrs: default=True
+ protect_attr: default=True

By default, ClassArgInit will set attributes directly on the calling class, using the argument name, with an "_" prefix for each argument in the calling functions' signature.

Setting set_attrs to False will prevent ClassArgInit from setting these class attributes.

Setting protect_attrs to False will cause the attributes to be set using the argument name, without a leading "_" character.

```python
from arg_init import ArgInit

class MyApp:
    def __init__(self, arg1=None):
        ClassArgInit(set_attrs=True, protect_attrs=False)
        ...
```

By default, ClassArgInit will set all arguments as protected class attributes of the MyApp instance. In the above example, arg1 will be available as an attribute "arg1" of the instance of MyApp.

### Support for kwargs

Support for kwargs in function signatures is provided via the argument **use_kwargs**. When this argument is set, any keword arguments would be initialised using the same resolution process as named arguments.

```python
from arg_init import FunctionArgInit

def my_func(self, **kwargs):
    args = FunctionArgInit(use_kwargs=True)
    ...
```
