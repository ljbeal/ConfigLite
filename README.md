# ConfigLite

A lightweight self-healing config handler.

## What is ConfigLite?

`ConfigLite` aims to provide a simple "subclass and go" methodology for handling yaml-based file configs.

Subclass from the base `BaseConfig` object and add your defaults.
Then, create an instance of your new class, providing a list of paths to search through.
If a config is found at once of these paths, it is used, otherwise a default config is created.

You can then set import this from wherever is needed and access properties.

For more details, see Usage below.

## Installation

### pypi

`ConfigLite` is available on pypi!

Simply run `pip install configlite` to install it in your current environment.

### development

If you want to make changes to how configs are handled, you can clone this repo and run `pip install -e .` to install it in editable mode.

> [!note]
> Find a bug? Feel free to make an issue or pull request!

## Usage

### Creating a Config

There are two methods of creating a config object.

#### Direct Initialisation

The simplest method to create a config, simply init the `BaseConfig` class and provide your defaults as an argument:

```python
from configlite import BaseConfig


CONFIG = BaseConfig(
    path = "config.yaml",
    defaults = {
        "value": 10,
        ...
    }
)
```

> [!tip]
> Here, you may pass a single `path`, or a list of `paths`. The config will search through each path until it finds a match (See the section on Paths below for more info).

#### As a Class

If you wish to add extra methods, create a subclass of the base `BaseConfig` object, adding your parameters and their defaults to a `defaults` field.

For example:

```python
from configlite import BaseConfig


class MyConfig(BaseConfig):
    defaults = {
        "value": 10,
        "name": "test",
        "pi": 3.14,
    }
```

You must still initialise the config, however:

```python
CONFIG = MyConfig(path="config.yaml")
```

### Access

To use your created config, there are two methods:

- "globally", where a single instance created.
- "locally", initialising the class where needed.

#### Global

To create a global config, set up the config as a parameter in the toplevel `__init__.py`:

```python
CONFIG = MyConfig("./path/to/config.yaml")
```

Then in the rest of your code you may import this object:

```python
from my_package import CONFIG

value = CONFIG.value
```

This is most useful if your code requires a single config file for everything.

#### Local

Or a local config, where you create an instance of your subclass wherever it is needed:

```python
from my_package import MyConfig

config = MyConfig("./path/to/config.yaml")

value = config.value
```

This can be useful if you are juggling multiple different config files dynamically.

> [!tip]
> This method is only recommended for subclasses, as each instance requires the same arguments.

## Paths

The `BaseConfig` object can take either a single path, or a list of paths.

If a list is passed, the config will search each one in order, using the last one in the list if none are found.

### Path Lists

Lets say you create a config this way:

```python
class Config(BaseConfig):
    ...

CONFIG = Config(
    paths=[
        "config.yaml",
        "~/.config/app/config.yaml",
    ]
)
```

In this case, `Config` will take these steps:

1. Search for `config.yaml` in the current working directory.
2. If not found, search for `~/.config/app/config.yaml`.
3. If still no file exists, create a default config at `~/.config/app/config.yaml`

If we get to step 3, but then create a new config at `./config.yaml`, this will take priority over the one found at `~/.config/app/config.yaml`.

## Environment Overrides

You may also set a `prefix` property, which enables environment overrides.

If we take our config from earlier, but add this feature:

```python
class MyConfig(BaseConfig):
    defaults = {
        "value": 10,
        "name": "test",
        "pi": 3.14,
    }
    prefix = "test_prefix"
```

Now, on initialisation, the config will search for environment variables starting with `test_prefix`

If we `export test_prefix_value="foo"`, we will see the changes:

```python
cfg = MyConfig(...)

cfg.value
> "foo"
```

> [!important]
> This is case-sensitive.

## Example

See `usage.py` for an example.
