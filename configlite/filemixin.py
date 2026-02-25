import os
from pathlib import Path
import shutil
from typing import Any

import yaml


class FileMixin:
    """Mixin class for handling file operations."""

    data = {}

    def __init__(
        self,
        path: Path | str | list[Path | str] | None = None,
        paths: list[Path | str] | None = None,
    ) -> None:
        """Provides methods for handling the file portion of the config.

        Args:
            path:
                The path to the config file. If the file does not exist, it will be created.
            paths:
                A list of paths to search for the config file.
                If it is not found in any, the last one in the list is used for creation.
        """
        if not path and not paths:
            raise ValueError("Either `path` or `paths` must be provided.")

        # Prioritise direct assignment
        self._paths = []
        if path is not None:
            # cover the case of BaseConfig(path=["a", "b"])
            if isinstance(path, (list, tuple)):
                for item in path:
                    self._paths.append(Path(item))
            else:
                self._paths.append(Path(path))

        if paths is not None:
            if not isinstance(paths, (list, tuple)) or len(paths) == 0:
                raise ValueError(
                    f"`paths` (type {type(paths)}) must be a valid list of paths"
                )
            for item in paths:
                self._paths.append(Path(item))

    @property
    def filename(self) -> str:
        """Filename, excluding path."""
        return self.path.name

    @property
    def path(self) -> Path:
        """Path to the config file."""
        return self._find_path()

    @property
    def abspath(self) -> Path:
        """Absolute path to the config file."""
        return self.path.resolve()

    def _ensure_dir(self) -> None:
        """Ensure that the directory for the config file exists."""
        dir_path = self.path.parent
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    def _ensure_file_integrity(self) -> bool:
        """Ensure that all attributes are present in the config file.

        Returns:
            bool: True if changes were made, False otherwise.

        """
        # if the file does not exist, we can get away with just writing the defaults
        if not self.path.exists():
            self._write(data=self.data, path=self.abspath)
            return True
        file_data = self._read()
        # remove deleted/renamed keys
        modified = False
        # need to first store targeted names and then iterate
        to_remove = []
        for key in file_data:
            if key not in self.data:
                to_remove.append(key)
        for key in to_remove:
            del file_data[key]
            modified = True
        # ensure missing keys are populated
        for attr, default in self.data.items():
            if attr not in file_data:
                file_data[attr] = default
                modified = True
        # if we made changes, write them
        if modified:
            self._write(file_data, self.abspath)
        return modified

    def _find_path(self) -> Path:
        """Dynamically find the path"""
        path_obj = None
        for path in self._paths:
            path_obj = Path(os.path.expandvars(str(path))).expanduser()
            if path_obj.exists():
                return path_obj
        if path_obj is None:
            raise FileNotFoundError(f"Path list is malformed: {self._paths}")
        return path_obj

    def _read(self) -> dict[str, Any]:
        """Read the config file and return its contents."""
        self._ensure_dir()
        with self.path.open("r") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            return data
        # In the case of a broken file, back it up and create a default one
        target_path = self.path
        backup_name = f"{self.filename}.bk"
        print(
            f"WARNING: Config file {target_path} failed to load.\n\tBacking up the file to: {backup_name}...",
            end=" ",
        )
        try:
            shutil.move(target_path, backup_name)
        except:
            print("Error.")
            raise

        print("Done.")
        return self._write(data=self.data, path=Path(target_path))

    def _write(self, data: dict[str, Any], path: Path) -> dict[str, Any]:
        """Explicitly write data to path."""
        self._ensure_dir()
        with path.open("w") as o:
            yaml.dump(data, o)

        return data
