import os
from pathlib import Path

import yaml

from configlite.config import BaseConfig
from tests.conftest import verify_variable


class ConfigTest(BaseConfig):
    defaults = {
        "foo": "foo",
    }


def test_default_to_last(tmpdir):
    """Tests that the default path is the last one in the list."""

    firstpath = tmpdir / "config_local.yaml"
    lastpath = tmpdir / ".config" / "config.yaml"

    config = ConfigTest(paths=[firstpath, lastpath])

    assert config.path == lastpath

    # now test that creating a config in the higher priority directories works
    with open(firstpath, "w+") as o:
        yaml.dump({"foo": "bar"}, o)

    assert config.path == firstpath
    assert config.foo == "bar"


def test_inner_dir_access(tmpdir):
    """Tests that configs in inner directories can be accessed."""
    inner_dir = tmpdir / "inner"
    cfg = ConfigTest(path=inner_dir / "config.yaml")

    assert inner_dir.exists()

    assert cfg.foo == "foo"
    verify_variable(cfg.path, "foo", "foo")


def test_stacked_files(tmpdir) -> None:
    """Test that specifying both path and paths does not cause problems."""
    cfg = ConfigTest(
        path=tmpdir / "config.yaml",
        paths=[tmpdir / "backup.yaml", tmpdir / "another.yaml"],
        autocreate=False,
    )

    assert len(cfg._paths) == 3
    assert cfg.paths[0] == tmpdir / "config.yaml"

    # check path list
    assert cfg.paths == [
        Path(p)
        for p in [
            tmpdir / "config.yaml",
            tmpdir / "backup.yaml",
            tmpdir / "another.yaml",
        ]
    ]
    # also add a check to ensure we _can_ get abspaths
    assert cfg.abspaths == [
        Path(p).resolve()
        for p in [
            tmpdir / "config.yaml",
            tmpdir / "backup.yaml",
            tmpdir / "another.yaml",
        ]
    ]
