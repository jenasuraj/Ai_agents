from __future__ import annotations

from collections.abc import Callable

from ai_agents.core.base import BaseAgent
from ai_agents.core.schemas import AgentInfo

AgentFactory = Callable[[], BaseAgent]


class AgentRegistry:
    """Simple in-memory registry for agent discovery and execution."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentFactory] = {}
        self._metadata: dict[str, AgentInfo] = {}

    def register(self, info: AgentInfo, factory: AgentFactory) -> None:
        if info.slug in self._agents:
            raise ValueError(f"Agent already registered: {info.slug}")

        self._agents[info.slug] = factory
        self._metadata[info.slug] = info

    def get(self, slug: str) -> BaseAgent:
        try:
            return self._agents[slug]()
        except KeyError as exc:
            available = ", ".join(sorted(self._agents)) or "none"
            raise KeyError(f"Unknown agent '{slug}'. Available agents: {available}") from exc

    def list_agents(self) -> list[AgentInfo]:
        return list(self._metadata.values())


registry = AgentRegistry()
