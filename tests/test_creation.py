from pathlib import Path

from configlite.config import BaseConfig


class MyConfig(BaseConfig):
    defaults = {"foo": "bar"}


def test_no_file_on_init() -> None:
    """Check that simply initialising a config does not create a file instantly."""
    file = Path("test.yaml")
    my_config = MyConfig(path=file)

    assert not file.exists()
    assert my_config.path == file
