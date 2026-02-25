import os
from pathlib import Path
from typing import Any
import pytest
import yaml

from configlite.config import BaseConfig


@pytest.fixture(scope="function", autouse=True)
def use_temp_dir(tmpdir):
    os.chdir(tmpdir)


@pytest.fixture(scope="function")
def simple_config():
    class SimpleConfig(BaseConfig):
        test = "foo"
    return SimpleConfig("test.yaml")


def verify_variable(file: Path, name: str, value: Any) -> bool:
    """Verify that a variable in the config file has the expected value.

    Args:
        file:
            The path to the config file.
        name:
            The name of the variable to check.
        value:
            The expected value of the variable.

    Returns:
        True if the variable has the expected value, False otherwise.

    """
    with file.open() as o:
        data = yaml.safe_load(o)

    return data.get(name, None) == value
