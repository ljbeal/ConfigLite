import os
from pathlib import Path

import yaml
from configlite.config import BaseConfig
from .conftest import verify_variable


class ConfigTest(BaseConfig):
    defaults = {
        "foo": "foo",
        "val": 10,
    }


def test_restore_file(capsys):
    file = Path("test.yaml")

    config = ConfigTest(file)

    with file.open("w+") as o:
        o.write("")  # create an empty file

    assert config.foo == "foo"
    assert config.val == 10

    assert os.path.exists(f"{file}.bk")
    assert "WARNING" in capsys.readouterr().out

    assert verify_variable(file, "foo", "foo")


def test_restore_file_priority(capsys):
    file_a = Path("test_a.yaml")
    file_b = Path("test_b.yaml")

    config = ConfigTest(paths=[file_a, file_b])

    with file_a.open("w+") as o:
        o.write("")  # create an empty file

    assert config.foo == "foo"
    assert config.val == 10

    assert os.path.exists(f"{file_a}.bk")
    assert "WARNING" in capsys.readouterr().out

    assert verify_variable(file_a, "foo", "foo")

def test_mangled_file(capsys):
    file = Path("test.yaml")

    config = ConfigTest(file)

    with file.open("w+") as o:
        o.write("foo")  # create a broken file

    assert config.foo == "foo"
    assert config.val == 10

    assert os.path.exists(f"{file}.bk")
    assert "WARNING" in capsys.readouterr().out


def test_delete_variable():
    file = Path("test.yaml")

    config = ConfigTest(file)

    assert config.foo == "foo"
    assert config.val == 10

    # get the file content for modification
    with file.open() as o:
        data = yaml.safe_load(o)
        assert data["foo"] == "foo"
    # delete foo and write the changes
    del data["foo"]
    with file.open("w+") as o:
        yaml.dump(data, o)
    # make sure it's gone
    assert not verify_variable(file, "foo", "foo")
    # we should still have the default value
    assert config.foo == "foo"
    # check that it's been added back to the config
    assert verify_variable(file, "foo", "foo")


def test_remove_variable():
    """Test that modifying the config updates the file correctly."""
    class ConfigTest_1(BaseConfig):
        defaults = {
            "foo": "foo",
            "bar": "bar",
        }

    class ConfigTest_2(BaseConfig):
        defaults = {
            "foo": "foo",
        }

    cfg = ConfigTest_1("test.yaml")
    assert cfg.foo == "foo"
    assert verify_variable(cfg.path, "foo", "foo")
    assert verify_variable(cfg.path, "bar", "bar")

    cfg = ConfigTest_2("test.yaml")
    assert verify_variable(cfg.path, "foo", "foo")
    assert not verify_variable(cfg.path, "bar", "bar")


def test_modify_variable():
    """Test that modifying the config updates the file correctly."""
    class ConfigTest_1(BaseConfig):
        defaults = {
            "foo": "foo",
        }

    class ConfigTest_2(BaseConfig):
        defaults = {
            "foo": "foo",
            "new": "new_value",
        }

    cfg = ConfigTest_1("test.yaml")
    assert cfg.foo == "foo"
    assert verify_variable(cfg.path, "foo", "foo")

    cfg = ConfigTest_2("test.yaml")
    assert verify_variable(cfg.path, "foo", "foo")
    assert verify_variable(cfg.path, "new", "new_value")
