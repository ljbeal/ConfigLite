import pytest

from configlite import BaseConfig


class ConfigTest(BaseConfig):
    defaults = {
        "INIT_VAR": "foo",
    }
    prefix = "MYPREFIX"


def test_override_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that we return the value of a set environment variable."""
    monkeypatch.setenv("MYPREFIX_INIT_VAR", "hello")
    cfg = ConfigTest(path="test_config.yaml")
    assert cfg.get("INIT_VAR") == "hello"


def test_missing_no_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that we're not just picking up any old variables."""
    monkeypatch.delenv("MYPREFIX_NONE_VAR", raising=False)
    cfg = ConfigTest(path="test_config.yaml")
    with pytest.raises(KeyError, match=".*not found in Config!"):
        cfg.get("NONE_VAR") is None


def test_missing_with_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that we can still default."""
    monkeypatch.delenv("MYPREFIX_NONE_VAR", raising=False)
    cfg = ConfigTest(path="test_config.yaml")
    assert cfg.get("NONE_VAR", "fallback") == "fallback"


def test_missing_with_default_on_class(monkeypatch: pytest.MonkeyPatch) -> None:
    """Returns the default value when the variable is not set."""
    monkeypatch.delenv("MYPREFIX_INIT_VAR", raising=False)
    cfg = ConfigTest(path="test_config.yaml")
    assert cfg.get("INIT_VAR") == "foo"
