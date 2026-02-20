from pathlib import Path
from typing import Any

from configlite.filemixin import FileMixin


class BaseConfig(FileMixin):
    """Lightweight Self-Healing config object."""

    def __init__(
        self, path: Path | str | None = None, paths: list[Path | str] | None = None
    ) -> None:
        """Initialize the config object.

        Args:
            path:
                The path to the config file. If the file does not exist, it will be created.
            paths:
                A list of paths to search for the config file.
                If it is not found in any, the last one in the list is used for creation.
        """
        super().__init__(path=path, paths=paths)

        self._attributes = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, property):
                continue
            if hasattr(v, "__call__"):
                continue
            if not k.startswith("_"):
                self._attributes[k] = v
                setattr(self, k, DeferredValue(k))

        if self.path.exists():
            self._ensure_file_integrity()

    def __getattribute__(self, name: str) -> Any:
        """Proxy attribute access. If the item is deferred, return the get instead."""
        item = object.__getattribute__(self, name)
        if isinstance(item, DeferredValue):
            return self.read(item.value)
        else:
            return item

    def __getitem__(self, key: str) -> Any:
        """Proxy subscript access to read method."""
        return self.read(key)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Expose the python `get` property."""
        if key in self.attributes:
            return self[key]
        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found in Config!")

    def read(self, attr: str) -> Any:
        """Read the config file and return its contents.

        If it does not exist, creates the file and fills it with default vaulues.
        """
        self._ensure_file_integrity()
        data = self._read()
        return data.get(attr)

    def write(self, path: Path | None = None) -> dict[str, Any]:
        """Write to the config, ignoring any existing values."""
        if path is None:
            path = self.abspath

        defaults = self._attributes.copy()
        if path.exists():
            defaults.update(self._read())
        self._write(data=defaults, path=path)
        return defaults

    @property
    def attributes(self) -> list[str]:
        """List of attributes that are defined in this config."""
        return [attr for attr in self._attributes.keys()]

    @property
    def defaults(self) -> dict[str, Any]:
        return self._attributes.copy()


class DeferredValue:
    """Stub class for deferring value access to a file read.

    Interacts with `__getattribute__` to "defer" reads to file.
    In Config, we first use the base object.__getattribute__(...) to collect an arbitrary item
    If that item has been replaced by a `DeferredValue` object, then we read from file
    Otherwise, return  the item

    Args:
        value (str): The name of the variable to access.
    """

    __slots__ = ["_parent", "_value"]

    def __init__(self, value: str) -> None:
        """Create the stub.

        Args:
            value: The name of the variable to access.
        """
        if not isinstance(value, str):
            raise TypeError("Value target must be a string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value
