from pathlib import Path
from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    foo: str = "foo"
    val: int = 10


def test_restore_file():
    file = Path("test.yaml")

    config = ConfigTest(file)

    with file.open("w+") as o:
        o.write("")  # create an empty file

    
    assert config.foo == "foo"
    assert config.val == 10
