from typing import ClassVar

import pytest

from configlite import BaseConfig


class ConfigTest(BaseConfig):
    defaults: ClassVar[dict] = {
        "INIT_VAR": "foo",
    }
    prefix = "MYPREFIX"


class ConfigTestUnderscore(BaseConfig):
    defaults: ClassVar[dict] = {
        "INIT_VAR": "foo",
    }
    prefix = "MYPREFIX_"


@pytest.mark.parametrize("cfg", [ConfigTest, ConfigTestUnderscore])
class TestEnvOverride:
    def test_override_with_env(self, cfg, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that we return the value of a set environment variable."""
        monkeypatch.setenv("MYPREFIX_INIT_VAR", "hello")
        cfg = cfg(path="test_config.yaml", autocreate=True)
        assert cfg.get("INIT_VAR") == "hello"
        assert cfg.INIT_VAR == "hello"
        assert cfg["INIT_VAR"] == "hello"

    def test_missing_no_default(self, cfg, monkeypatch: pytest.MonkeyPatch) -> None:
        """Check that we're not just picking up any old variables."""
        monkeypatch.delenv("MYPREFIX_NONE_VAR", raising=False)
        cfg = cfg(path="test_config.yaml", autocreate=True)
        with pytest.raises(KeyError, match=".*not found in Config!"):
            cfg.get("NONE_VAR") is None

    def test_missing_with_default(self, cfg, monkeypatch: pytest.MonkeyPatch) -> None:
        """Check that we can still default."""
        monkeypatch.delenv("MYPREFIX_NONE_VAR", raising=False)
        cfg = cfg(path="test_config.yaml", autocreate=True)
        assert cfg.get("NONE_VAR", "fallback") == "fallback"

    def test_missing_with_default_on_class(
        self, cfg, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Returns the default value when the variable is not set."""
        monkeypatch.delenv("MYPREFIX_INIT_VAR", raising=False)
        cfg = cfg(path="test_config.yaml", autocreate=True)
        assert cfg.get("INIT_VAR") == "foo"
        assert cfg.INIT_VAR == "foo"
        assert cfg["INIT_VAR"] == "foo"

    def test_get_reads_current_env(self, cfg, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that `get` reflects the true state of the environment."""
        cfg = cfg(path="test_config.yaml", autocreate=True)
        monkeypatch.setenv("MYPREFIX_INIT_VAR", "hello")
        assert cfg.get("INIT_VAR") == "hello"
        assert cfg.INIT_VAR == "hello"
        assert cfg["INIT_VAR"] == "hello"
