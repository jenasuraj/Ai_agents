from __future__ import annotations
from ai_agents.core.registry import registry


CLI_TITLE = "Suraj Agent Lab"


def main() -> None:
    """Basic CLI entrypoint for discovering registered agents."""

    print(CLI_TITLE)

    agents = registry.list_agents()

    if not agents:
        print("No registered agents found in the shared registry.")
        print("Experimental agents still live inside the projects/ folder.")
        return

    print("Available registered agents:")
    for agent in agents:
        print(f"- {agent.slug}: {agent.name}")


if __name__ == "__main__":
    main()
