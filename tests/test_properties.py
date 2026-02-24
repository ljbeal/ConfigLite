import pytest
from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    defaults = {
        "foo": "foo",
    }


class ConfigWithMethods(BaseConfig):
    defaults = {
        "foo": "foo",
    }

    def some_method(self) -> str:
        return "bar"


class ConfigWithProperty(BaseConfig):
    defaults = {
        "foo": "foo",
    }

    @property
    def some_property(self) -> str:
        return "bar"


@pytest.mark.parametrize(
    "config_class",
    [
        ConfigTest,
        ConfigWithMethods,
        ConfigWithProperty,
    ]
)
def test_attributes(config_class) -> None:
    """Tests that the attributes property returns the correct list of attributes."""

    config = config_class("config.yaml")

    assert "foo" in config.attributes
