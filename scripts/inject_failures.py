from storage.sqlite_memory import SQLiteAdvisoryMemory
from storage.outcomes import FAILURE

memory = SQLiteAdvisoryMemory()

TASK = "Parse and summarize a malformed JSON file"
TOOLS = ["filesystem.read", "json.parse"]

for _ in range(5):
    memory.record_task(
        task_description=TASK,
        tools=TOOLS,
        outcome=FAILURE,
        domain="data-processing",
        constraints=["untrusted-input"],
    )

print("Injected failure history.")
