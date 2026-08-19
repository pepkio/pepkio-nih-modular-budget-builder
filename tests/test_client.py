"""Unit tests for PepkioClient using mocked HTTP responses."""

from __future__ import annotations

import pytest

from pepkio_nih_modular_budget_builder.client import PepkioClient
from pepkio_nih_modular_budget_builder.config import DEFAULT_API_BASE_URL, TOOL_ID
from pepkio_nih_modular_budget_builder.exceptions import PepkioAPIError
from pepkio_nih_modular_budget_builder.models import ModularBudgetInput, RunResult


def test_client_init_defaults():
    client = PepkioClient(api_key="test-key")
    assert client.base_url == DEFAULT_API_BASE_URL
    client.close()


def test_client_require_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "load_example"})


def test_get_manifest_mock(httpx_mock):
    mock_manifest = {
        "schema_version": "1.0",
        "tool_id": TOOL_ID,
        "title": "NIH Modular Budget Builder",
        "examples": [
            {"name": "load_example", "input": {"action": "load_example"}},
            {"name": "calculate_r01", "input": {"action": "calculate"}},
        ],
    }
    httpx_mock.add_response(
        url=f"{DEFAULT_API_BASE_URL}/api/tools/v1/tools/{TOOL_ID}/manifest",
        json=mock_manifest,
    )

    with PepkioClient(api_key="test-key") as client:
        manifest = client.get_manifest()
        assert manifest["tool_id"] == TOOL_ID
        assert client.list_examples() == ["load_example", "calculate_r01"]
        assert client.get_example_input("load_example") == {"action": "load_example"}


def test_run_mock(httpx_mock):
    httpx_mock.add_response(
        url=f"{DEFAULT_API_BASE_URL}/api/tools/v1/tools/{TOOL_ID}/run",
        json={
            "run_id": "run-123",
            "status": "completed",
            "result": {"budget": {"fiscalYear": 2026}},
            "error": None,
            "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run-123",
            "permalink": "https://tools.pepkio.com/r/run-123",
        },
    )

    with PepkioClient(api_key="test-key") as client:
        res = client.run({"action": "load_example"})
        assert isinstance(res, RunResult)
        assert res.run_id == "run-123"
        assert res.status == "completed"
        assert res.result == {"budget": {"fiscalYear": 2026}}


def test_run_with_pydantic_model_mock(httpx_mock):
    httpx_mock.add_response(
        url=f"{DEFAULT_API_BASE_URL}/api/tools/v1/tools/{TOOL_ID}/run",
        json={
            "run_id": "run-456",
            "status": "completed",
            "result": {"budget": {}},
            "error": None,
        },
    )

    with PepkioClient(api_key="test-key") as client:
        inp = ModularBudgetInput(action="load_example")
        res = client.run(inp)
        assert res.run_id == "run-456"


def test_run_error_response_mock(httpx_mock):
    httpx_mock.add_response(
        url=f"{DEFAULT_API_BASE_URL}/api/tools/v1/tools/{TOOL_ID}/run",
        status_code=400,
        json={
            "error": {
                "message": "Invalid budget input",
                "code": "INVALID_INPUT",
            }
        },
    )

    with PepkioClient(api_key="test-key") as client:
        with pytest.raises(PepkioAPIError) as exc_info:
            client.run({"action": "invalid"})
        assert exc_info.value.status_code == 400
        assert exc_info.value.code == "INVALID_INPUT"
        assert "Invalid budget input" in str(exc_info.value)


def test_get_run_mock(httpx_mock):
    httpx_mock.add_response(
        url=f"{DEFAULT_API_BASE_URL}/api/tools/v1/runs/run-789",
        json={
            "run_id": "run-789",
            "status": "completed",
            "result": {"status": "ok"},
            "error": None,
        },
    )

    with PepkioClient(api_key="test-key") as client:
        res = client.get_run("run-789")
        assert res.run_id == "run-789"
        assert res.status == "completed"
