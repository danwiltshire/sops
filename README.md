# sops

CLI-driven SOP manager powered by the GitHub Copilot SDK.

Write a symptom and resolution, and sops generates a structured SOP document and raises a pull request against your SOP repository — all from the terminal.

[![CI](https://github.com/danwiltshire/sops/actions/workflows/ci.yml/badge.svg)](https://github.com/danwiltshire/sops/actions/workflows/ci.yml)

## Installation

```bash
pip install sops
```

Requires Python 3.11+. Authenticate with GitHub before first use:

```bash
gh auth login
```

## Quick start

Point sops at your SOP repository, then record your first entry:

```bash
sops config set sop-repository owner/repo

sops edit payments --service refunds
```

Your editor opens with a template. Fill in the symptom and the steps to resolve it, save, and sops generates the SOP and raises a PR.

## Commands

### `sops edit <app> [--service <service>]`

Record a new SOP entry for an application (and optionally a specific service). Opens your editor twice — once for the problem, once for the resolution — then raises a PR against the configured repository.

```bash
sops edit datadog --service api
```

### `sops context <app> [--service <service>]`

Add or update background context for an application. This context is stored as `CONTEXT.md` in the app directory and is read by the `ask` command to provide more accurate answers.

```bash
sops context datadog
```

### `sops ask <app> <question>`

Ask a question about an application using its SOP content. The model reads all SOP and context files for the app from the repository and answers based solely on that content.

```bash
sops ask datadog "Why am I getting rate limited on /v1/metrics?"
```

### `sops list`

List all SOPs available in the configured repository.

```bash
sops list
```

### `sops config set <key> <value>` / `sops config get <key>`

Read and write sops configuration. Config is stored at `~/.config/sops/config.json`.

```bash
sops config set sop-repository owner/repo
sops config get sop-repository
```

#### Configuration keys

| Key              | Description                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| `sop-repository` | GitHub repository (`owner/repo`) where SOPs are stored. Required by all commands except `config`. |

## Repository structure

sops expects (and maintains) this layout in the SOP repository:

```
{app}/
  SOP.md          ← used when no --service is provided
  {service}.md    ← used when --service is provided
  CONTEXT.md      ← background context written by `sops context`
```

## Authentication

sops reads a GitHub token in the following order:

1. `GITHUB_TOKEN` environment variable
2. `gh auth token` (GitHub CLI)

The token must have permission to read and write to the SOP repository.

## Developing

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
uv sync
uv run pre-commit install
```

### Running tests

```bash
uv run pytest tests/ -v
```

### Linting

[Ruff](https://docs.astral.sh/ruff/) is configured in `pyproject.toml`. Pre-commit runs it automatically on every commit.

To run manually:

```bash
uv run pre-commit run --all-files
```
