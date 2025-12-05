# ConfigLite

A lightweight self-healing config handler.

Subclass from the base `BaseConfig` object and add your variables and defaults.

You can then set import this from wherever is needed and access properties.


## Installation

`git clone` this repository, then use `pip install .` to install it in your current environment.


## Examples

### Setup
Create a subclass of the base `BaseConfig` object, adding your parameters and their defaults.

For example:

```python
from configlite import BaseConfig


class MyConfig(BaseConfig):
    value: int = 10
    name: str = "test"
    pi: float = 3.14
```

### Usage
You are then free to import this subclass wherever. You can use a "global" method, where a single instance is passed around. Otherwise, you can initialise the class where needed.

#### Global

A "global" config, where you set up the config as a parameter in the toplevel `__init__.py`:
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

#### Example

See `usage.py` for full example.
