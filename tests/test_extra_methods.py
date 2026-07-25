from typing import ClassVar

from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    defaults: ClassVar[dict] = {
        "test_value": 42,
        "name": "Test_Name",
    }

    @property
    def uppercase_name(self) -> str:
        return self.name.upper()


def test_extra_methods():
    config = ConfigTest(path="test.yaml")
    assert config.name == "Test_Name"
    assert config.uppercase_name == "TEST_NAME"
