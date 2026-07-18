from pathlib import Path

import yaml

from configlite import BaseConfig
from tests.conftest import verify_variable


class ConfigTest(BaseConfig):
    defaults = {
        "foo": "foo",
    }


def test_autocreate_false_creates_no_file() -> None:
    """Test that autocreate=False does not instantly create the file."""
    cfg = ConfigTest(path="test_config.yaml", autocreate=False)
    assert not cfg.abspath.exists()


def test_autocreate_true_creates_file() -> None:
    """Test that setting autocreate=True will automatically create the last file in the list."""
    cfg = ConfigTest(path="test_config.yaml", autocreate=True)
    assert cfg.abspath.exists()
    verify_variable(cfg.path, "foo", "foo")


def test_autocreate_true_creates_last_file() -> None:
    """Test that setting autocreate=True will automatically create the last file in the list."""
    cfg = ConfigTest(path=["priority.yaml", "test_config.yaml"], autocreate=True)
    assert cfg.abspath.exists()
    assert cfg.path.name == "test_config.yaml"
    verify_variable(cfg.path, "foo", "foo")


def test_autocreate_does_not_overwrite_files() -> None:
    """Test that using autocreate does not overwrite already existing files."""
    last_file = Path("test_config.yaml")
    with last_file.open("w+") as o:
        yaml.dump({"foo": "bar"}, o)
    cfg = ConfigTest(path=["priority.yaml", "test_config.yaml"], autocreate=True)

    assert cfg.abspath.exists()
    assert cfg.path == last_file
    assert cfg.foo == "bar"

    verify_variable(last_file, "foo", "bar")


def test_autocreate_does_not_overwrite_priority_files() -> None:
    """Test that using autocreate does not overwrite files that are higher in the path list."""
    priority_file = Path("priority.yaml")
    with priority_file.open("w+") as o:
        yaml.dump({"foo": "bar"}, o)
    cfg = ConfigTest(path=["priority.yaml", "test_config.yaml"], autocreate=True)

    assert cfg.abspath.exists()
    assert cfg.path == priority_file
    assert cfg.foo == "bar"

    verify_variable(priority_file, "foo", "bar")
