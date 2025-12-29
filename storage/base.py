from typing import List, Dict, Any


class AdvisoryMemoryBase:
    def record_task(
        self,
        task_description: str,
        tools: List[str],
        outcome: str,
        domain: str | None,
        constraints: List[str] | None,
    ) -> None:
        raise NotImplementedError

    def tool_stats(self, tool: str) -> Dict[str, int]:
        raise NotImplementedError

    def all_tasks(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
