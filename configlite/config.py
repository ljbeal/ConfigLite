from pathlib import Path
from typing import Any

from configlite.filemixin import FileMixin


class BaseConfig(FileMixin):
    """Lightweight Self-Healing config object."""

    defaults: dict[str, Any] = {}

    def __init__(
        self,
        path: Path | str | list[Path | str] | None = None,
        paths: list[Path | str] | None = None,
        defaults: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the config object.

        Args:
            path (str, Path): The path to the config file. If the file does not exist, it will be created.
            paths (list[str | Path]):
                A list of paths to search for the config file.
                If it is not found in any, the last one in the list is used for creation.
            defaults (dict): Default values for the config. Overrides any set at the class level.
        """
        super().__init__(path=path, paths=paths)

        # init with the hardcoded defaults
        self.data = self.defaults.copy()
        if defaults:
            self.data.update(defaults)

        if self.path.exists():
            self._ensure_file_integrity()

    def __getattribute__(self, name: str) -> Any:
        """Proxy attribute access. If the item is deferred, return the get instead."""
        if (
            name not in ["attributes", "data"]
            and hasattr(self, "data")
            and name in self.data
        ):
            return self.get(name)
        else:
            return object.__getattribute__(self, name)

    def __getitem__(self, key: str) -> Any:
        """Proxy subscript access to read method."""
        return self.get(key)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Expose the python `get` property.

        If the key exists within the attributes, it is read from file.
        Otherwise, the default value is returned. If no default is provided, a KeyError is raised.
        """
        # prefer file read
        if self.abspath.exists():
            self._ensure_file_integrity()

            file_data = self._read()
            if key in file_data:
                return file_data[key]
            if default:
                return default
        # fallback to internal data
        if key in self.data:
            val = self.data.get(key)
            # update file
            self._ensure_file_integrity()
            return val
        # otherwise, default, but don't write to file
        if default:
            return default
        raise KeyError(f"Key '{key}' not found in Config!")

    @property
    def attributes(self) -> list[str]:
        """List of attributes that are defined in this config."""
        return list(self.data)
