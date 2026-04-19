import json
from pathlib import Path

import click

_CONFIG_PATH = Path(click.get_app_dir("sops")) / "config.json"


def _read_config() -> dict:
    if _CONFIG_PATH.exists():
        return json.loads(_CONFIG_PATH.read_text())
    return {}


def _write_config(data: dict) -> None:
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_PATH.write_text(json.dumps(data, indent=2))


def _require_config(key: str) -> str:
    value = _read_config().get(key)
    if not value:
        raise click.ClickException(
            f"Config key '{key}' is not set. Run: sops config set {key} <value>"
        )
    return value
