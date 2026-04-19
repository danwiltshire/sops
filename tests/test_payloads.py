import json
import re
from unittest.mock import patch

from sops.utils.payloads import build_context_payload, build_sop_payload


def test_build_sop_payload_with_service():
    with patch("sops.utils.payloads._run_id", return_value="20260419120000"):
        result = json.loads(
            build_sop_payload("owner/repo", "payments", "refunds", "503 errors", "Rolled back")
        )

    assert result["sop_repository"] == "owner/repo"
    assert result["application"] == "payments"
    assert result["service"] == "refunds"
    assert result["problem_statement"] == "503 errors"
    assert result["problem_resolution"] == "Rolled back"
    assert result["run_id"] == "20260419120000"


def test_build_sop_payload_without_service():
    with patch("sops.utils.payloads._run_id", return_value="20260419120000"):
        result = json.loads(
            build_sop_payload("owner/repo", "payments", None, "503 errors", "Rolled back")
        )

    assert result["service"] is None


def test_build_context_payload_with_service():
    with patch("sops.utils.payloads._run_id", return_value="20260419120000"):
        result = json.loads(
            build_context_payload("owner/repo", "datadog", "api", "Metrics ingestion service")
        )

    assert result["sop_repository"] == "owner/repo"
    assert result["application"] == "datadog"
    assert result["service"] == "api"
    assert result["description"] == "Metrics ingestion service"
    assert result["run_id"] == "20260419120000"


def test_build_context_payload_without_service():
    with patch("sops.utils.payloads._run_id", return_value="20260419120000"):
        result = json.loads(
            build_context_payload("owner/repo", "datadog", None, "Metrics ingestion service")
        )

    assert result["service"] is None


def test_run_id_format():
    from sops.utils.payloads import _run_id

    run_id = _run_id()
    assert re.fullmatch(r"\d{14}", run_id), f"run_id '{run_id}' does not match expected format"
