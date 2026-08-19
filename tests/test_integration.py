"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import httpx
import pytest

from pepkio_nih_modular_budget_builder.client import PepkioClient
from pepkio_nih_modular_budget_builder.exceptions import PepkioAPIError

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")

    # Probe environment with a 1-second timeout to avoid long hangs if local server is down
    probe_timeout = 1.0 if "localtest.me" in base_url else 10.0
    client = PepkioClient(api_key=api_key, base_url=base_url, timeout=probe_timeout)
    try:
        manifest = client.get_manifest(refresh=True)
        if manifest.get("tool_id") != "nih-modular-budget-builder":
            pytest.skip(f"Tool manifest not returned as expected on {env_name}")
    except (httpx.HTTPError, PepkioAPIError, Exception) as exc:
        pytest.skip(f"Live API unreachable or failed on {env_name} ({base_url}): {exc}")

    yield client
    client.close()


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "nih-modular-budget-builder"
    names = live_client.list_examples()
    assert "load_example" in names
    assert "calculate_r01" in names
    assert "effort_check" in names


def test_run_load_example(live_client: PepkioClient):
    inp = live_client.get_example_input("load_example")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("error") is None


def test_run_calculate_r01(live_client: PepkioClient):
    inp = live_client.get_example_input("calculate_r01")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    res = result.result.get("result")
    assert isinstance(res, dict)
    assert "years" in res
    assert len(res["years"]) == 5
    assert "personnelJustification" in res


def test_run_effort_check(live_client: PepkioClient):
    inp = live_client.get_example_input("effort_check")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    effort = result.result.get("effort")
    assert isinstance(effort, dict)
    assert "overCommitted" in effort
