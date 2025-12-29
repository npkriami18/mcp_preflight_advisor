from schemas.input import AdvisoryInput
from schemas.output import AdvisoryResponse, ToolSuggestion, AdvisoryWarning
from advisor.rules import apply_rules
from advisor.scoring import (
    compute_overall_confidence,
    adjust_confidence_with_history,
)
from advisor.risk import risk_warnings_for_tool
from storage.memory import InMemoryAdvisoryMemory

memory = InMemoryAdvisoryMemory()


def advise(input: AdvisoryInput) -> AdvisoryResponse:
    suggestions, warnings, explanation = apply_rules(input)

    all_warnings = list(warnings)

    for s in adjusted:
        tool_warnings = risk_warnings_for_tool(s.tool_name, memory)
        all_warnings.extend(tool_warnings)

    adjusted = []
    for s in suggestions:
        adjusted_conf = adjust_confidence_with_history(s, memory)
        adjusted.append(
            s.copy(update={"confidence": adjusted_conf})
        )

    overall_confidence = compute_overall_confidence(adjusted, all_warnings)

    return AdvisoryResponse(
        suggested_sequence=adjusted,
        overall_confidence=overall_confidence,
        warnings=all_warnings,
        explanation=explanation,
        evidence_summary="Historical outcomes influenced confidence and warnings.",
    )

