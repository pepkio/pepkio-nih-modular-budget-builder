# SPDX-License-Identifier: MIT
"""Typed API request/response models derived from live tool manifest."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .exceptions import PepkioAPIError


class PersonnelMember(BaseModel):
    """Personnel entry in budget."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    role: str | None = None
    appointmentType: Literal["calendar", "academic"] | str | None = None
    ibs: float | None = None
    effortPercent: float | None = None
    fringeRatePercent: float | None = None


class CostsConfig(BaseModel):
    """Budget costs configuration."""

    model_config = ConfigDict(extra="allow")

    faRatePercent: float | None = None
    equipment: float | None = None
    consortiumDirect: float | None = None
    consortiumFa: float | None = None
    otherDirect: float | None = None
    escalationRatePercent: float | None = None
    projectYears: int | None = Field(default=None, ge=1, le=5)


class BudgetInput(BaseModel):
    """Budget data for calculation."""

    model_config = ConfigDict(extra="allow")

    fiscalYear: int | None = None
    personnel: list[PersonnelMember] | None = None
    costs: CostsConfig | None = None


class EffortGrant(BaseModel):
    """Grant effort ledger entry."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    efforts: dict[str, float] | None = None


class ModularBudgetInput(BaseModel):
    """Tool input model for nih-modular-budget-builder."""

    model_config = ConfigDict(extra="allow")

    action: Literal["calculate", "export_csv", "load_example", "effort_check"] | str | None = None
    budget: BudgetInput | None = None
    effortGrants: list[EffortGrant] | None = None


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        raise PepkioAPIError(
            err.get("message", "Tool run failed"),
            code=err.get("code"),
            details=err.get("details") if isinstance(err.get("details"), dict) else {},
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)
