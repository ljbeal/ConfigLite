from pathlib import Path
from typing import ClassVar

import pytest
import yaml

from configlite.config import BaseConfig
from tests.conftest import verify_variable


class ConfigTest(BaseConfig):
    defaults: ClassVar[dict] = {
        "foo": "foo",
    }


def test_no_args() -> None:
    """Tests that an error is raised when no paths are provided."""

    with pytest.raises(ValueError):
        ConfigTest()


def test_path_as_list() -> None:
    """Tests that providing path as a list works."""
    paths = ["config1.yaml", "config2.yaml"]

    config = ConfigTest(path=paths)  # pyright: ignore[reportArgumentType]
    assert config._paths == [Path(p) for p in paths]
    assert config.path == Path("config2.yaml")
    assert config.filename == "config2.yaml"


def test_paths_as_empty_list() -> None:
    """Tests that providing paths as an empty list raises an error."""

    with pytest.raises(ValueError):
        ConfigTest(paths=[])


def test_path_as_paths() -> None:
    """Tests that providing path in place of paths raises an error."""

    with pytest.raises(ValueError):
        ConfigTest(paths="config.yaml")  # type: ignore


def test_file_adoption() -> None:
    """Ensures that a pre-existing file is not overwritten by a new config creation."""
    file = Path("precreate.yaml")
    with file.open("w+") as o:
        yaml.safe_dump({"foo": "bar"}, o)

    cfg = ConfigTest(file)

    assert cfg.foo == "bar"
    assert cfg["foo"] == "bar"
    assert verify_variable(file, "foo", "bar")


def test_init_with_modified_defaults() -> None:
    """Tests that providing modified defaults works."""
    file = Path("config.yaml")
    cfg = ConfigTest(path=file, defaults={"foo": "bar"})

    assert cfg.foo == "bar"
    assert cfg["foo"] == "bar"
    assert verify_variable(file, "foo", "bar")


def test_init_with_extra_defaults() -> None:
    """Tests that providing extra defaults works."""
    file = Path("config.yaml")
    cfg = ConfigTest(path=file, defaults={"foo": "bar", "new": "new"})

    assert cfg.new == "new"
    assert cfg["new"] == "new"
    assert verify_variable(file, "new", "new")
