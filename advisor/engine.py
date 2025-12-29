from schemas.input import AdvisoryInput
from schemas.output import AdvisoryResponse, ToolSuggestion, AdvisoryWarning
from advisor.rules import apply_rules
from advisor.scoring import (
    compute_overall_confidence,
    adjust_confidence_with_history,
)
from advisor.risk import risk_warnings_for_tool
from advisor.similarity import find_similar_tasks
from storage.memory import InMemoryAdvisoryMemory
from storage.sqlite_memory import SQLiteAdvisoryMemory

memory = SQLiteAdvisoryMemory()



def advise(input: AdvisoryInput) -> AdvisoryResponse:
    suggestions, warnings, explanation = apply_rules(input)

    adjusted = []
    for s in suggestions:
        adjusted_conf = adjust_confidence_with_history(s, memory)
        adjusted.append(
            s.copy(update={"confidence": adjusted_conf})
        )
    all_warnings = list(warnings)

    for s in adjusted:
        tool_warnings = risk_warnings_for_tool(s.tool_name, memory)
        all_warnings.extend(tool_warnings)

    overall_confidence = compute_overall_confidence(adjusted, all_warnings)

    current_task = {
        "task": input.task_description,
        "tools": input.available_tools,
        "domain": input.domain,
        "constraints": input.constraints or [],
    }

    similar = find_similar_tasks(current_task, memory.all_tasks())

    evidence_summary = None
    if similar:
        evidence_summary = (
            f"Found {len(similar)} similar past task(s). "
            f"Most recent outcome: {similar[0]['outcome']}."
        )

    return AdvisoryResponse(
        suggested_sequence=adjusted,
        overall_confidence=overall_confidence,
        warnings=all_warnings,
        explanation=explanation,
        evidence_summary=evidence_summary,
    )

