from sqlite_utils import Database
from storage.base import AdvisoryMemoryBase
from storage.outcomes import SUCCESS, FAILURE, UNKNOWN
from typing import List, Dict, Any
import json


class SQLiteAdvisoryMemory(AdvisoryMemoryBase):
    def __init__(self, path: str = "advisory.db"):
        self.db = Database(path)

        self.db["tasks"].create(
            {
                "id": int,
                "task": str,
                "tools": str,
                "outcome": str,
                "domain": str,
                "constraints": str,
            },
            pk="id",
            if_not_exists=True,
        )

    def record_task(
        self,
        task_description: str,
        tools: List[str],
        outcome: str,
        domain: str | None,
        constraints: List[str] | None,
    ) -> None:
        self.db["tasks"].insert(
            {
                "task": task_description,
                "tools": json.dumps(tools),
                "outcome": outcome,
                "domain": domain,
                "constraints": json.dumps(constraints or []),
            }
        )

    def tool_stats(self, tool: str) -> Dict[str, int]:
        rows = self.db.query(
            """
            SELECT outcome, COUNT(*) as count
            FROM tasks, json_each(tasks.tools)
            WHERE json_each.value = :tool
            GROUP BY outcome
            """,
            {"tool": tool},
        )

        stats = {SUCCESS: 0, FAILURE: 0, UNKNOWN: 0}
        for row in rows:
            stats[row["outcome"]] = row["count"]
        return stats

    def all_tasks(self) -> List[Dict[str, Any]]:
        rows = self.db["tasks"].rows
        return [
            {
                "task": r["task"],
                "tools": json.loads(r["tools"]),
                "outcome": r["outcome"],
                "domain": r["domain"],
                "constraints": json.loads(r["constraints"]),
            }
            for r in rows
        ]
