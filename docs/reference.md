# Reference

## ClassArgInit

```python
ClassArgInit(env_prefix=None, priority=ENV_PRIORITY, use_kwargs=False, set_attrs=True, protect_atts=True, defaults=None)
```

Resolve argument values using the bound function that calls ClassArgInit as the reference. Process each argument (skipping the first argument as this is a class reference) from the calling function, resolving and storing the value in a dictionary, where the argument name is the key.

### Arguments

+ **env_prefix**: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must include this prefix followed by an "_" character and the name of the argument.

+ **priority**: By default arguments will be set based on the priority env, arg, default. An alternate priority of arg, env, default is available by setting priority=ARG_PRIORITY.

+ **use_kwargs**: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

+ **set_attrs**: Set the arguments as class attributes. Default is true.

+ **protect_attrs**: Add a leading "_" character to all assigned attribute names. Default is True.

+ **defaults**: A list of ArgDefault objects.

### Attributes

#### args

An object representing the resolved arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a [python-box](https://github.com/cdgriffith/Box) Box class.

## FunctionArgInit

```python
FunctionArgInit(env_prefix=None, priority=ENV_PRIORITY, use_kwargs=False, defaults=None)
```

Resolve argument values using the function that calls FunctionArgInit as the reference. Process each argument from the calling function, resolving and storing the value in a dictionary, where the argument name is the key.

### Arguments

+ **env_prefix**: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must include this prefix followed by an "_" character and the name of the argument.

+ **priority**: By default arguments will be set based on the priority env, arg, default. An alternate priority of arg, env, default is available by setting priority=ARG_PRIORITY.

+ **use_kwargs**: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

+ **defaults**: A list of ArgDefault objects.

### Attributes

#### args

An object representing the resolved arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a [python-box](https://github.com/cdgriffith/Box) Box class.

### ArgDefaults

```python
ArgDefaults(name, default_value=None, env_name="", disable_env=False)
```

A class that can be used to modify settings for an individual argument.

### Arguments

+ **env_name**: The name of the associated environment variable. If not set, env defaults to the uppercase equivalent of the argument name.

+ **default_value**: The default value to be applied if both arg and env values are not used.

+ **disable_env**: If True then do not consider the env value when resolving the value.
