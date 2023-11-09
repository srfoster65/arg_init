# Reference

## ClassArgInit

```python
ClassArgInit(priorities=DEFAULT_PRIORITY, env_prefix=None, use_kwargs=False, defaults=None, config="config", set_attrs=True, protect_atts=True)
```

Resolve argument values using the bound function that calls ClassArgInit as the reference. Process each argument (skipping the first argument as this is a class reference) from the calling function, resolving and storing the value in a dictionary, where the argument name is the key.

### Arguments

+ **priorities**: By default arguments will be set based on the priority sequence: config, env, arg, default. Several alternate priority sequences are predefined, or a custom sequence can be defined.

+ **env_prefix**: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must include this prefix followed by an "_" character and the name of the argument.

+ **use_kwargs**: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

+ **defaults**: A list of ArgDefault objects.

+ **config**: The name of the config file to load defaults from. If this is a Path object it can be a relative or absolute path to a config file. If a string, it can be the name of the file (excluding the extension). Default is to search for a file named "config" in the current working directory.

+ **set_attrs**: Set the arguments as class attributes. Default is true.

+ **protect_attrs**: Add a leading "_" character to all assigned attribute names. Default is True.

### Attributes

#### args

An object representing the resolved arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a [python-box](https://github.com/cdgriffith/Box) Box class.

## FunctionArgInit

```python
FunctionArgInit(env_prefix=None, priority=DEFAULT_PRIORITY, use_kwargs=False, defaults=None, config="config")
```

Resolve argument values using the function that calls FunctionArgInit as the reference. Process each argument from the calling function, resolving and storing the value in a dictionary, where the argument name is the key.

### Arguments

+ **priorities**: By default arguments will be set based on the priority sequence:  config, env, arg, default. Several alternate priority sequences are predefined, or a custom sequence can be defined.
+ 
+ **env_prefix**: env_prefix is used to avoid namespace clashes with environment variables. If set, all environment variables must include this prefix followed by an "_" character and the name of the argument.

+ **use_kwargs**: When initialising arguments, only named arguments will be initialised by default. If use_kwargs=True, then any keyword arguments will also be initialised

+ **defaults**: A list of ArgDefault objects.

+ **config**: The name of the config file to load defaults from. If this is a Path object it can be a relative or absolute path to a config file. If a string, it can be the name of the file (excluding the extension). Default is to search for a file named "config" in the current working directory.

### Attributes

#### args

An object representing the resolved arguments. Arguments are exposed as attributes or key/value pairs.

Note: The returned object is a [python-box](https://github.com/cdgriffith/Box) Box class.

### ArgDefaults

```python
ArgDefaults(name, default_value=None, env_name="")
```

A class that can be used to modify settings for an individual argument.

### Arguments

+ **env_name**: The name of the associated environment variable. If not set, env defaults to the uppercase equivalent of the argument name.

+ **default_value**: The default value to be applied if both arg and env values are not used.

## Priorities

### Priority Sequences

A prioity sequence defines the resolution priority when resolving argument values. It is a list of Priority eunums.

The following priority sequences are defined:

+ CONFIG_PRIORITY = CONFIG, ENV, ARG, DEFAULT
+ ENV_PRIORITY = ENV, CONFIG, ARG, DEFAULT
+ ARG_PRIORITY = ARG, CONFIG, ENV, DEFAULT

DEFAULT_PRIORITY = CONFIG_PRIORITY

The following Priority values are defined:

+ Priority.CONFIG
+ Priority.ENV
+ Priority.ARG
+ Priority.DEFAULT

These values can be used to define a custom priority sequence. If a Priority is omitted, then it will not be used in the resolution process.

e.g.

```python
priorities = list(Priority.ENV, Priority.ARG, Priority.DEFAULT)
```

Will define a priority sequence that does not use a config file during the resolution process.
