import subprocess
from unittest.mock import MagicMock, patch

import click
import pytest

from sops.utils.agent import _github_mcp, _github_token, _load_prompt


def test_github_token_reads_env_var():
    with patch.dict("os.environ", {"GITHUB_TOKEN": "env-token"}):
        assert _github_token() == "env-token"


def test_github_token_falls_back_to_gh_cli():
    mock_result = MagicMock()
    mock_result.stdout = "cli-token\n"
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("subprocess.run", return_value=mock_result) as mock_run,
    ):
        token = _github_token()
    mock_run.assert_called_once_with(
        ["gh", "auth", "token"], capture_output=True, text=True, check=True
    )
    assert token == "cli-token"


def test_github_token_raises_when_gh_fails():
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gh")),
        pytest.raises(click.ClickException, match="No GitHub token found"),
    ):
        _github_token()


def test_github_token_raises_when_gh_not_found():
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("subprocess.run", side_effect=FileNotFoundError),
        pytest.raises(click.ClickException, match="No GitHub token found"),
    ):
        _github_token()


def test_github_mcp_structure():
    mcp = _github_mcp("my-token")
    assert "github" in mcp
    assert mcp["github"]["type"] == "http"
    assert mcp["github"]["url"] == "https://api.githubcopilot.com/mcp/"
    assert mcp["github"]["headers"]["Authorization"] == "Bearer my-token"
    assert mcp["github"]["tools"] == ["*"]


def test_load_prompt_returns_file_contents():
    with patch("pathlib.Path.read_text", return_value="Hello world"):
        result = _load_prompt("test_message")
    assert result == "Hello world"
