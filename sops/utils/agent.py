import asyncio
import os
import subprocess
from pathlib import Path

import click
from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType
from copilot.session import PermissionHandler


def _github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(  # noqa: S603
            ["gh", "auth", "token"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise click.ClickException(
            "No GitHub token found. Set GITHUB_TOKEN or authenticate with `gh auth login`."
        ) from exc


def _load_prompt(name: str) -> str:
    return (Path(__file__).parent.parent / "system_messages" / f"{name}.md").read_text()


def _github_mcp(token: str) -> dict:
    return {
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {"Authorization": f"Bearer {token}"},
            "tools": ["*"],
        }
    }


async def _agent(prompt: str, system_message: str, token: str) -> str:
    chunks: list[str] = []
    async with CopilotClient() as client:
        session = await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-4.1",
            system_message={"mode": "append", "content": system_message},
            mcp_servers=_github_mcp(token),
            streaming=True,
        )

        def handle_event(event):
            if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                chunks.append(event.data.delta_content)

        session.on(handle_event)
        await session.send_and_wait(prompt, timeout=300.0)
    return "".join(chunks)


def _run_agent(prompt: str, system_message: str, token: str) -> str:
    try:
        return asyncio.run(_agent(prompt=prompt, system_message=system_message, token=token))
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
