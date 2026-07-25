import os
from pathlib import Path
from typing import Any, ClassVar

from configlite.filemixin import FileMixin


class BaseConfig(FileMixin):
    """Lightweight Self-Healing config object."""

    defaults: ClassVar[dict[str, Any]] = {}
    prefix: str | None = None

    def __init__(
        self,
        path: Path | str | list[Path] | list[str] | None = None,
        paths: list[Path | str] | None = None,
        defaults: dict[str, Any] | None = None,
        autocreate: bool = True,
    ) -> None:
        """Initialize the config object.

        Args:
            path (str, Path): The path to the config file.
            paths (list[Path | str]):
                A list of paths to search for the config file.
                If it is not found in any, the last one in the list is used for creation.
            defaults (dict): Default values for the config. Overrides any set at the class level.
            autocreate (bool): Ensure that the file exists at init
        """
        super().__init__(path=path, paths=paths, autocreate=autocreate)

        # init with the hardcoded defaults
        self.data = self.defaults.copy()
        if defaults:
            self.data.update(defaults)
            self._ensure_file_integrity(overwrite=True)

        elif self.path.exists():
            self._ensure_file_integrity()

        if not self.abspath.exists() and autocreate:
            self._ensure_file_integrity(overwrite=True)

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

    def _get_env(self, key: str) -> str | None:
        """Check the environment for a prefixed override.

        Uses the prefix to search. For example, if we have prefix=PREFIX, and search for key="FOO",
        Perform a check for PREFIX_FOO
        """
        if self.prefix is None:
            return None
        normalised = self.prefix if self.prefix.endswith("_") else f"{self.prefix}_"
        return os.environ.get(f"{normalised}{key}", None)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Expose the python `get` property.

        If the key exists within the attributes, it is read from file.
        Otherwise, the default value is returned. If no default is provided, a KeyError is raised.
        """
        # check env overrides first
        from_env = self._get_env(key)
        if from_env is not None:
            return from_env

        # prefer file read
        if self.abspath.exists():
            self._ensure_file_integrity()

            file_data = self._read()
            if key in file_data:
                return file_data[key]
            if default is not None:
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
