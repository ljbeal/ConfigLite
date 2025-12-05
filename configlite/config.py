from pathlib import Path
from typing import Any
import yaml


class Config:
    """Lightweight Self-Healing config object."""

    def __init__(self, path: Path | str) -> None:
        """Initialize the config object.

        Args:
           path: The path to the config file. If the file does not exist, it will be created.
        """
        self._path = Path(path)

        self._attributes = {}
        for k, v in self.__class__.__dict__.items():
            if k in Config.__dict__:
                continue
            if not k.startswith("_"):
                self._attributes[k] = v
                setattr(self, k, DeferredValue(k))

    def __getattribute__(self, name: str) -> Any:
        """Proxy attribute access. If the item is deferred, return the get instead."""
        item = object.__getattribute__(self, name)
        if isinstance(item, DeferredValue):
            return self.read()[item.value]
        else:
            return item

    @property
    def filename(self) -> str:
        """Filename, excluding path."""
        return self._path.name

    @property
    def path(self) -> Path:
        """Path to the config file."""
        return self._path

    def _read(self) -> dict[str, Any]:
        """Read the config file and return its contents."""
        with self.path.open("r") as f:
            return yaml.safe_load(f)

    def read(self) -> dict[str, Any]:
        """Read the config file and return its contents.

        If it does not exist, creates the file and fills it with default vaulues.
        """
        if not self.path.exists():
            self.write()
        return self._read()

    def write(self) -> None:
        """Write to the config, ignoring any existing values."""
        defaults = self._attributes.copy()
        if self.path.exists():
            defaults.update(self._read())
        with self.path.open("w+") as f:
            yaml.dump(defaults, f)

    @property
    def attributes(self) -> list[str]:
        """List of attributes that are defined in this config."""
        return [attr for attr in self._attributes.keys()]


class DeferredValue:
    """Stub class for deferring value access."""

    __slots__ = ["_parent", "_value"]

    def __init__(self, value: str) -> None:
        """Create the stub.

        Args:
            parent: The Config object that owns this value.
            value: The name of the variable to access.
        """
        if not isinstance(value, str):
            raise TypeError("Value target must be a string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value
