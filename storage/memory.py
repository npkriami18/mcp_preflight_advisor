from typing import List, Dict, Any
from collections import defaultdict
from storage.outcomes import SUCCESS, FAILURE, UNKNOWN


class InMemoryAdvisoryMemory:
    def __init__(self):
        # key: tool_name → stats
        self.tool_stats = defaultdict(
            lambda: {SUCCESS: 0, FAILURE: 0, UNKNOWN: 0}
        )
        self.task_history: List[Dict[str, Any]] = []

    def record(
        self,
        task_description: str,
        tools: List[str],
        outcome: str = UNKNOWN,
        domain: str | None = None,
        constraints: List[str] | None = None,
    ):
        self.task_history.append(
            {
                "task": task_description,
                "tools": tools,
                "outcome": outcome,
                "domain": domain,
                "constraints": constraints or [],
            }
        )

        for tool in tools:
            self.tool_stats[tool][outcome] += 1

    def stats_for(self, tool: str) -> Dict[str, int]:
        return self.tool_stats.get(
            tool,
            {SUCCESS: 0, FAILURE: 0, UNKNOWN: 0},
        )
    
    def all_tasks(self) -> List[Dict[str, Any]]:
        return self.task_history
