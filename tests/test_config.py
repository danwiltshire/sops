import json
from unittest.mock import patch

import click
import pytest

from sops.utils.config import _read_config, _require_config, _write_config


@pytest.fixture
def config_path(tmp_path):
    path = tmp_path / "config.json"
    with patch("sops.utils.config._CONFIG_PATH", path):
        yield path


def test_read_config_returns_empty_dict_when_missing(config_path):
    assert _read_config() == {}


def test_write_and_read_config(config_path):
    _write_config({"sop-repository": "owner/repo"})
    assert _read_config() == {"sop-repository": "owner/repo"}


def test_write_config_creates_parent_dirs(tmp_path):
    path = tmp_path / "nested" / "dir" / "config.json"
    with patch("sops.utils.config._CONFIG_PATH", path):
        _write_config({"key": "value"})
    assert path.exists()
    assert json.loads(path.read_text()) == {"key": "value"}


def test_require_config_returns_value(config_path):
    _write_config({"sop-repository": "owner/repo"})
    assert _require_config("sop-repository") == "owner/repo"


def test_require_config_raises_when_missing(config_path):
    with pytest.raises(click.ClickException, match="sop-repository"):
        _require_config("sop-repository")


def test_require_config_raises_when_empty_string(config_path):
    _write_config({"sop-repository": ""})
    with pytest.raises(click.ClickException, match="sop-repository"):
        _require_config("sop-repository")
