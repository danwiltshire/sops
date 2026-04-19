import json
from datetime import UTC, datetime


def _run_id() -> str:
    return datetime.now(UTC).strftime("%Y%m%d%H%M%S")


def build_sop_payload(
    repo: str, app: str, service: str | None, problem: str, resolution: str
) -> str:
    return json.dumps(
        {
            "sop_repository": repo,
            "application": app,
            "service": service,
            "problem_statement": problem,
            "problem_resolution": resolution,
            "run_id": _run_id(),
        },
        indent=2,
    )


def build_context_payload(repo: str, app: str, service: str | None, description: str) -> str:
    return json.dumps(
        {
            "sop_repository": repo,
            "application": app,
            "service": service,
            "description": description,
            "run_id": _run_id(),
        },
        indent=2,
    )
