from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    foo: str = "foo"


def test_attributes() -> None:
    """Tests that the attributes property returns the correct list of attributes."""

    config = ConfigTest("config.yaml")

    assert "foo" in config.attributes
