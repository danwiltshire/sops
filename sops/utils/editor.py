import click

PROBLEM_TEMPLATE = """\


# Describe the symptom or trigger condition.
# Lines starting with # are ignored.
#
# Example:
#   GET /v1/metrics returns HTTP 429 (Too Many Requests) for all callers.
#   Alert: 'API rate limit exceeded' fires in PagerDuty.
"""

RESOLUTION_TEMPLATE = """\


# Describe the steps to resolve the issue.
# Lines starting with # are ignored.
#
# Example:
#   1. Check rate-limit counters: `kubectl exec -n api -- redis-cli GET rl:global`.
#   2. If limit is misconfigured, update the quota in the api-gateway ConfigMap.
#   3. Restart the api-gateway pod and confirm GET /v1/metrics returns 200.
"""

CONTEXT_TEMPLATE = """\


# Describe the application — its purpose, infrastructure, and any useful context.
# Lines starting with # are ignored.
#
# Example:
#   The Datadog integration service ingests metrics from our Kubernetes clusters and
#   forwards them to Datadog via the API. It runs as a Deployment in the 'monitoring'
#   namespace, scaled to 3 replicas, and is configured via the 'datadog-config' ConfigMap.
#   Alerts are routed through PagerDuty to the platform on-call rotation.
"""


def _strip_comments(text: str) -> str:
    lines = []

    for line in text.splitlines():
        if not line.startswith("#"):
            lines.append(line)

    return "\n".join(lines).strip()


def _edit_prompt(template: str, error: str) -> str:
    raw = click.edit(template, extension=".md")
    text = _strip_comments(raw) if raw else ""
    if not text:
        raise click.ClickException(error)
    return text
