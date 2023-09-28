# Reference

## ArgInit

```python
ArgInit(env_prefix="", priority=ARG_PRIORITY, use_kwargs=False, args=None)
```

Initialise arguments using the function that calls ArgInit as the reference. Process each argument, setting the value of the class dictionary, args, with either the value provided by the argument, an associated environment variable or a default value. If the value of the arg or env is None then try the next item in the selected priority system

env_prefix: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must have include this prefix followed by an "_" character and the name of the argument.

priority: By default arguments will be set based on the prioty env, arg, default. An alternate priority of arg, env, default is available by setting priority=ARG_PRIORITY.

use_kwargs: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

args: A list of Arg objects that allow overriding the processing behaviour of individual arguments.

### Methods

set(object)

Set the attributes of **object** using the args dictionary. The key is used as the attribute name and the value is assigned assigned to the attribute.
If there is a namespace clash in object (i.e. An attribute with the same name as an argument already exists) an AttributeExistsError will be raised

### Attributes

args

An object representing the processed arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a python-box Box class.

## Arg

```python
Arg(name, env=None, default=None, attr=None, force_arg=False, force_env=True, force_default=True, disable_env=False)
```

A dataclass that is used to customise the processing of arguments.

+ **name**: (required) The name of the argument.

+ **env**: The name of the associated environment variable. Only required if different from the argument name. This value should not include any "env_prefix"

+ **default**: The default value to be applied if both arg and env values are not used

+ **attr**: If set then the value of the argument in the args dictionary will use this name as the key instead of the arg name

+ **force_arg**: If True, set the value if the arg value is None

+ **force_env**: If True, set the value if the env value is ""

+ **force_default**: If False, and the default value is None then no argument will be set in the args dictionary.

## AttributeExistsError

Raised if attempting to set an attribute of an object, and an attribute with the same name already exists.

```python
AttributeExistsError(arg)
```
