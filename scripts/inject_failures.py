from storage.sqlite_memory import SQLiteAdvisoryMemory
from storage.outcomes import FAILURE

sqlite_memory_instance = SQLiteAdvisoryMemory()

TASK = "Parse and summarize a malformed JSON file"
TOOLS = ["filesystem.read", "json.parse"]

for _ in range(5):
    sqlite_memory_instance.record_task(
        task_description=TASK,
        tools=TOOLS,
        outcome=FAILURE,
        domain="data-processing",
        constraints=["untrusted-input"],
    )

print("Injected failure history.")
