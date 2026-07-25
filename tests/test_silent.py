from typing import ClassVar

from configlite.config import BaseConfig


class Config(BaseConfig):
    defaults: ClassVar[dict] = {"foo": "foo"}


def test_silent(capsys) -> None:
    """Checks that we don't print anything."""
    cfg = Config(path="test.yaml")
    assert cfg.foo == "foo"

    stdout = capsys.readouterr().out
    print(stdout)
    assert stdout == ""
