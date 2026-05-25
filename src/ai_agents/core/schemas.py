from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Standard execution status returned by every agent."""

    SUCCESS = "success"
    ERROR = "error"


class AgentRequest(BaseModel):
    """Common input model for all agents."""

    query: str = Field(..., min_length=1, description="User request or task for the agent.")
    agent_type: str = Field(..., min_length=1, description="Registered agent identifier.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Common output model for all agents."""

    status: AgentStatus
    agent_type: str
    output: str
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class AgentInfo(BaseModel):
    """Public metadata used to document and discover agents."""

    name: str
    slug: str
    description: str
    entrypoint: str | None = None
    tools: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
