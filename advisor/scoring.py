from typing import List
from schemas.output import ToolSuggestion, AdvisoryWarning
from storage.sqlite_memory import SQLiteAdvisoryMemory
from storage.outcomes import SUCCESS, FAILURE



def compute_overall_confidence(
    suggestions: List[ToolSuggestion],
    warnings: List[AdvisoryWarning],
) -> float:
    if not suggestions:
        return 0.1

    base = sum(s.confidence for s in suggestions) / len(suggestions)

    penalty = 0.0
    for w in warnings:
        if w.severity == "high":
            penalty += 0.3
        elif w.severity == "caution":
            penalty += 0.1

    return max(0.0, min(1.0, base - penalty))

def adjust_confidence_with_history(
    suggestion: ToolSuggestion,
    sqlite_memory: SQLiteAdvisoryMemory,
) -> float:
    stats = sqlite_memory.tool_stats(suggestion.tool_name)

    successes = stats[SUCCESS]
    failures = stats[FAILURE]

    total = successes + failures
    if total < 3:
        # insufficient evidence
        return suggestion.confidence

    historical_rate = successes / total

    # conservative blend: history nudges, never dominates
    return (suggestion.confidence * 0.7) + (historical_rate * 0.3)
