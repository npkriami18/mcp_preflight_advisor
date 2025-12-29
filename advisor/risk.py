from schemas.output import AdvisoryWarning
from storage.memory import InMemoryAdvisoryMemory
from storage.outcomes import SUCCESS, FAILURE


def risk_warnings_for_tool(
    tool_name: str,
    memory: InMemoryAdvisoryMemory,
) -> list[AdvisoryWarning]:
    stats = memory.tool_stats(tool_name)

    successes = stats[SUCCESS]
    failures = stats[FAILURE]
    total = successes + failures

    if total < 3:
        return []

    if failures >= successes * 2:
        return [
            AdvisoryWarning(
                code="HISTORICAL_FAILURE_BIAS",
                message=(
                    f"Tool '{tool_name}' has failed {failures} "
                    f"out of {total} recent recorded uses."
                ),
                severity="high",
            )
        ]

    if failures > successes:
        return [
            AdvisoryWarning(
                code="ELEVATED_FAILURE_RATE",
                message=(
                    f"Tool '{tool_name}' shows a higher failure rate "
                    f"({failures}/{total}) than success."
                ),
                severity="caution",
            )
        ]

    return []
