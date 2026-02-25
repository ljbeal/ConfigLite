import os
from pathlib import Path

import pytest
from configlite.filemixin import FileMixin


@pytest.mark.parametrize(
    "path",
    [
        "$HOME/config.yaml",
        "~/config.yaml",
    ]
)
def test_home_expansion(path: str) -> None:
    """Tests that paths are properly expanded."""

    config = FileMixin(paths=[path])

    expected_path = Path(os.path.expanduser("~")) / "config.yaml"

    assert config.path == expected_path


def test_arbitrary_variable() -> None:
    """Tests that arbitrary environment variables are expanded."""

    os.environ["CONFIGLITE_TEST_PATH"] = "config_env.yaml"

    config = FileMixin(paths=["$CONFIGLITE_TEST_PATH"])

    expected_path = Path(os.getcwd()) / "config_env.yaml"

    assert config.abspath == expected_path


def test_inner_dir():
    """Tests that paths in inner directories are properly resolved."""
    cfg = FileMixin(path="inner/config.yaml")

    assert cfg.abspath == Path(os.getcwd()) / "inner" / "config.yaml"


def test_malformed_paths():
    """Tests that malformed paths raise an error.

    This is a rare condition that requires some level of clobbering,
    but we test it to make pylance happy.
    """
    config = FileMixin(paths=["config.yaml"])

    config._paths = []
    with pytest.raises(FileNotFoundError):
        config.path


def test_path_stacking():
    """Check that specifying both path and paths creates a list."""
    config = FileMixin(path="1", paths=["2", "3"])

    assert config._paths == [Path(p) for p in ["1", "2", "3"]]
