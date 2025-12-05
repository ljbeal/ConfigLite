from pathlib import Path
from configlite import BaseConfig
import yaml


class MyConfig(BaseConfig):
    context: int = 8192
    name: str = "test"
    pi: float = 3.14


if __name__ == "__main__":
    configpath = Path("config.yaml")

    if configpath.exists():
        configpath.unlink()

    my_config = MyConfig(configpath)

    print(f"context: {my_config.context}")
    print(f"name: {my_config.name}")

    modified_vals = {"context": 16384, "name": "foo"}
    with open(configpath, "w+") as f:
        yaml.dump(modified_vals, f)

    print(f"context: {my_config.context}")
    print(f"name: {my_config.name}")
