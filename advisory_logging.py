from rich.console import Console
import sys
from rich.table import Table

console = Console(file=sys.stderr)


def log_advisory(input, response):
    table = Table(title="Preflight Advisory Decision")

    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Task", input.task_description)
    table.add_row("Tools", ", ".join(input.available_tools))
    table.add_row("Confidence", f"{response.overall_confidence:.2f}")
    table.add_row("Warnings", str(len(response.warnings)))
    table.add_row("Explanation", response.explanation)

    console.print(table)
