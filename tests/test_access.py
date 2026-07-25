from typing import ClassVar

import pytest

from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    defaults: ClassVar[dict] = {"foo": "foo"}


def test_attribute_access():
    cfg = ConfigTest("test_config.yaml")

    assert cfg.foo == "foo"


def test_subscript_access():
    cfg = ConfigTest("test_config.yaml")

    assert cfg["foo"] == "foo"


def test_get() -> None:
    """Test the `get` method."""
    cfg = ConfigTest("test_config.yaml")

    assert cfg.get("foo") == "foo"


def test_get_nonexistent() -> None:
    """Check that we raise an error on a nonexistent get, with no default."""
    cfg = ConfigTest("test_config.yaml")

    with pytest.raises(KeyError):
        cfg.get("blah")


def test_get_nonexistent_with_default() -> None:
    """Check that get defaulting works."""
    cfg = ConfigTest("test_config.yaml")

    assert cfg.get("blah", "foo") == "foo"
