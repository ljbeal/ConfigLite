from pathlib import Path
from typing import Any

from configlite.filemixin import FileMixin


class BaseConfig(FileMixin):
    """Lightweight Self-Healing config object."""

    defaults: dict[str, Any] = {}

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
        # init with the hardcoded defaults
        self.data = self.defaults.copy()

        if self.path.exists():
            self._ensure_file_integrity()

    def __getattribute__(self, name: str) -> Any:
        """Proxy attribute access. If the item is deferred, return the get instead."""
        if (
            name not in ["attributes", "defaults"]
            and hasattr(self, "defaults")
            and name in self.defaults
        ):
            return self.read(name)
        else:
            return object.__getattribute__(self, name)

    def __getitem__(self, key: str) -> Any:
        """Proxy subscript access to read method."""
        return self.read(key)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Expose the python `get` property."""
        if key in self.attributes:
            return self.read(key)
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
        return list(self.data)


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
