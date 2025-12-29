from collections import defaultdict
from typing import List, Dict
from storage.outcomes import SUCCESS, FAILURE, UNKNOWN


class InMemoryAdvisoryMemory:
    def __init__(self):
        # key: tool_name → stats
        self.tool_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {SUCCESS: 0, FAILURE: 0, UNKNOWN: 0}
        )

    def record(
        self,
        tool_sequence: List[str],
        outcome: str = UNKNOWN,
    ) -> None:
        for tool in tool_sequence:
            self.tool_stats[tool][outcome] += 1

    def stats_for(self, tool: str) -> Dict[str, int]:
        return self.tool_stats.get(
            tool,
            {SUCCESS: 0, FAILURE: 0, UNKNOWN: 0},
        )
