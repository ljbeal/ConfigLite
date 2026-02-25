from configlite.config import BaseConfig


class ConfigA(BaseConfig):
    defaults = {"param1": "value1"}


class ConfigB(BaseConfig):
    """Simulate updating the config to include a new parameter."""
    defaults = {
        "param1": "value1",
        "param2": "value2",
    }


def test_update_config():
    cfg = ConfigA("config.yaml")

    assert cfg.param1 == "value1"

    assert cfg.path.exists()

    # Simulate updating the config class to add a new parameter"
    cfg = ConfigB("config.yaml")
    assert cfg.param1 == "value1"
    assert cfg.param2 == "value2"
