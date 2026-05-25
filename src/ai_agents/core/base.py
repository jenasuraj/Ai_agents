from __future__ import annotations

from abc import ABC, abstractmethod

from ai_agents.core.schemas import AgentInfo, AgentRequest, AgentResponse


class BaseAgent(ABC):
    """Base contract every production-ready agent should follow.

    Existing experimental agents can be gradually migrated to this interface.
    The goal is to keep all agents consistent in how they receive input,
    execute work, and return output.
    """

    info: AgentInfo

    @abstractmethod
    def run(self, request: AgentRequest) -> AgentResponse:
        """Execute the agent and return a standardized response."""
        raise NotImplementedError
