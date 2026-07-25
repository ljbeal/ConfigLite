from typing import ClassVar

import yaml

from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    defaults: ClassVar[dict] = {
        "test": "foo",
    }


def test_ensure_empty() -> None:
    assert BaseConfig("test.yaml").attributes == []


def test_attributes() -> None:
    class TestConfig(BaseConfig):
        defaults: ClassVar[dict] = {"test": 10}

    assert TestConfig("test.yaml").attributes == ["test"]


def test_update() -> None:
    config = ConfigTest("test.yaml")

    with open(config.abspath, "w+") as o:
        yaml.dump({"test": "bar"}, o)

    print(type(config.test))

    assert config.test == "bar"
    assert config.get("test") == "bar"
