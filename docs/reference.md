# Reference

## ArgInit

```python
ArgInit(env_prefix="", priority=ARG_PRIORITY, use_kwargs=False, func_is_bound=False, set_attrs=True, args=None)
```

Initialise arguments using the function that calls ArgInit as the reference. Process each argument, setting the value of the class dictionary, args, with either the value provided by the argument, an associated environment variable or a default value. If the value of the arg or env is None then try the next item in the selected priority system

### Arguments

+ **env_prefix**: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must have include this prefix followed by an "_" character and the name of the argument.

+ **priority**: By default arguments will be set based on the prioty env, arg, default. An alternate priority of arg, env, default is available by setting priority=ARG_PRIORITY.

+ **use_kwargs**: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

+ **is_class**: Set to True if the function being processed is a class method i.e. the first argument is "self"

+ **set_attrs**: If the function being processed is a class method (a bound function), set the arguments as class attributes. Default is true. Set to false to disable. This attribute has no effect if is_class=False.

+ **args**: A list of Arg objects that allow overriding the processing behaviour of individual arguments.

### Attributes

#### args

An object representing the processed arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a [python-box](https://github.com/cdgriffith/Box) Box class.

## Arg

```python
Arg(name, env=None, default=None, attr=None, force_arg=False, force_env=True, disable_env=False)
```

A dataclass that is used to customise the processing of arguments.

### Arguments

+ **name**: (required) The name of the argument.

+ **env**: The name of the associated environment variable. If not set, env defaults to the uppercase equivalent of the argument name.

+ **default**: The default value to be applied if both arg and env values are not used.

+ **attr**: The name of the argument in the args dictionary. Setting this value allows the argument to be referenced by a different name to that of the argument. If not set, defaults to the argument name

+ **force_arg**: If True, set the value if the arg value is None

+ **force_env**: If True, set the value if the env value is "" (an empty string)

+ **disable_env**: If True then do not consider the env value when resolving the value.

### Methods

+ **resolve**

Important: This method is only intended to be called by ArgInit.

Resolve a value for the Arg using the specified priority system.

```python
resolve(self, priority=DEFAULT_PRIORITY_SYSTEM)
```

## AttributeExistsError

Raised if attempting to set an attribute of an object and an attribute with the same name already exists.

```python
AttributeExistsError(Exception)
```
