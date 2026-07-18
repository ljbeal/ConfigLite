from pathlib import Path

from configlite.config import BaseConfig


class MyConfig(BaseConfig):
    defaults = {"foo": "bar"}


def test_file_on_init() -> None:
    """Check that initialising a config does create a file instantly."""
    file = Path("test.yaml")
    my_config = MyConfig(path=file)

    assert file.exists()
    assert my_config.path == file
