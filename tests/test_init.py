from pathlib import Path
import pytest
import yaml
from configlite.config import BaseConfig
from tests.conftest import verify_variable


class ConfigTest(BaseConfig):
    defaults = {
        "foo": "foo",
    }


def test_no_args() -> None:
    """Tests that an error is raised when no paths are provided."""

    with pytest.raises(ValueError):
        ConfigTest()


def test_path_as_list() -> None:
    """Tests that providing path as a list works."""

    config = ConfigTest(path=["config1.yaml", "config2.yaml"])
    assert config._paths == ["config1.yaml", "config2.yaml"]
    assert config.path == Path("config2.yaml")
    assert config.filename == "config2.yaml"


def test_paths_as_empty_list() -> None:
    """Tests that providing paths as an empty list raises an error."""

    with pytest.raises(ValueError):
        ConfigTest(paths=[])


def test_paths_as_paths() -> None:
    """Tests that providing paths as a valid list works."""

    with pytest.raises(ValueError):
        ConfigTest(paths="config.yaml")


def test_empty_paths():
    """Tests that providing empty paths raises an error."""
    with pytest.raises(ValueError):
        ConfigTest(paths=[])


def test_file_adoption() -> None:
    """Ensures that a pre-existing file is not overwritten by a new config creation."""
    file = Path("precreate.yaml")
    with file.open("w+") as o:
        yaml.safe_dump({"foo": "bar"}, o)

    cfg = ConfigTest(file)

    assert cfg.foo == "bar"
    assert cfg["foo"] == "bar"
    assert verify_variable(file, "foo", "bar")
