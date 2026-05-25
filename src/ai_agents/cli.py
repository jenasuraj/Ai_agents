from __future__ import annotations

from ai_agents.core.registry import registry


def main() -> None:
    """Basic CLI entrypoint for discovering registered agents."""

    agents = registry.list_agents()

    if not agents:
        print("No agents registered yet.")
        print("Existing experimental agents still live inside the projects/ folder.")
        return

    print("Available agents:")
    for agent in agents:
        print(f"- {agent.slug}: {agent.name}")


if __name__ == "__main__":
    main()
