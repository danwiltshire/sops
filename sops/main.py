import click
from halo import Halo
from rich.console import Console
from rich.markdown import Markdown

from .utils.agent import _github_token, _load_prompt, _run_agent
from .utils.config import _read_config, _require_config, _write_config
from .utils.editor import CONTEXT_TEMPLATE, PROBLEM_TEMPLATE, RESOLUTION_TEMPLATE, _edit_prompt
from .utils.payloads import build_context_payload, build_sop_payload

service_option = click.option("--service", default=None, help="Service name within the app.")


@click.group()
def cli():
    """sops — Standard Operating Procedure manager."""
    pass


@cli.group()
def config():
    """Manage sops configuration."""
    pass


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Set a configuration value."""
    data = _read_config()
    data[key] = value

    _write_config(data)

    click.echo(f"{key} = {value}")


@config.command("get")
@click.argument("key")
def config_get(key: str) -> None:
    """Get a configuration value."""
    value = _read_config().get(key)

    if value is None:
        raise click.ClickException(f"Config key '{key}' is not set.")

    click.echo(value)


@cli.command()
@click.argument("app")
@service_option
def edit(app: str, service: str | None) -> None:
    """Record a new SOP entry for APP (and optionally a SERVICE)."""
    repo = _require_config("sop-repository")
    location = f"{app}/{service}" if service else app

    click.echo(f"New SOP entry: {location}")

    problem = _edit_prompt(PROBLEM_TEMPLATE, "No problem provided — aborted.")
    resolution = _edit_prompt(RESOLUTION_TEMPLATE, "No resolution provided — aborted.")

    with Halo(text="Raising PR...", spinner="dots"):
        response = _run_agent(
            prompt=build_sop_payload(repo, app, service, problem, resolution),
            system_message=_load_prompt("edit_system_message"),
            token=_github_token(),
        )
    click.echo(f"PR: {response.strip()}")


@cli.command()
@click.argument("app")
@service_option
def context(app: str, service: str | None) -> None:
    """Add or update background context for APP (and optionally a SERVICE)."""
    repo = _require_config("sop-repository")
    location = f"{app}/{service}" if service else app

    click.echo(f"Updating context: {location}")

    description = _edit_prompt(CONTEXT_TEMPLATE, "No input provided — aborted.")

    with Halo(text="Raising PR...", spinner="dots"):
        response = _run_agent(
            prompt=build_context_payload(repo, app, service, description),
            system_message=_load_prompt("context_system_message"),
            token=_github_token(),
        )
    click.echo(f"PR: {response.strip()}")


@cli.command("list")
def list_sops() -> None:
    """List available SOPs in the configured repository."""
    repo = _require_config("sop-repository")

    with Halo(text="Fetching SOPs...", spinner="dots"):
        response = _run_agent(
            prompt=f"sop_repository: {repo}",
            system_message=_load_prompt("list_system_message"),
            token=_github_token(),
        )
    click.echo(response.strip())


@cli.command()
@click.argument("app")
@click.argument("question")
def ask(app: str, question: str) -> None:
    """Ask a question about APP using its SOP content."""
    repo = _require_config("sop-repository")

    with Halo(text="Searching SOPs...", spinner="dots"):
        response = _run_agent(
            prompt=f"Repository: {repo}\nApplication directory: {app}\n\nQuestion: {question}",
            system_message=_load_prompt("ask_system_message"),
            token=_github_token(),
        )

    Console().print(Markdown(response))


if __name__ == "__main__":
    cli()
