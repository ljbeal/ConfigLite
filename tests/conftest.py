import os
import pytest

from configlite.config import Config


@pytest.fixture(scope="function", autouse=True)
def use_temp_dir(tmpdir):
    os.chdir(tmpdir)


@pytest.fixture(scope="function")
def simple_config():
    class SimpleConfig(Config):
        test = "foo"
    return SimpleConfig("test.yaml")
