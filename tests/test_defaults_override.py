from configlite.config import BaseConfig
from tests.conftest import verify_variable


class Config(BaseConfig):
    defaults = {
        "foo": "foo"
    }


CONFIG = {
    "foo": "bar"
}


def test_update_when_file() -> None:
    """Make sure we can update a config when a file already exists."""
    cfg = Config(path="foo.yaml")
    assert cfg.foo == "foo"
    assert cfg["foo"] == "foo"
    assert verify_variable(cfg.abspath, "foo", "foo")

    assert cfg.abspath.exists()

    print("Creating with new defaults")
    cfg = Config(path="foo.yaml", defaults=CONFIG)

    assert cfg.foo == "bar"
    assert cfg["foo"] == "bar"
    assert verify_variable(cfg.abspath, "foo", "bar")
