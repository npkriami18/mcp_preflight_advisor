from schemas.input import AdvisoryInput
from schemas.output import AdvisoryResponse, ToolSuggestion, AdvisoryWarning
from advisor.rules import apply_rules
from advisor.scoring import (
    compute_overall_confidence,
    adjust_confidence_with_history,
)
from storage.memory import InMemoryAdvisoryMemory

memory = InMemoryAdvisoryMemory()


def advise(input: AdvisoryInput) -> AdvisoryResponse:
    suggestions, warnings, explanation = apply_rules(input)

    adjusted = []
    for s in suggestions:
        adjusted_conf = adjust_confidence_with_history(s, memory)
        adjusted.append(
            s.copy(update={"confidence": adjusted_conf})
        )

    overall_confidence = compute_overall_confidence(adjusted, warnings)

    return AdvisoryResponse(
        suggested_sequence=adjusted,
        overall_confidence=overall_confidence,
        warnings=warnings,
        explanation=explanation,
        evidence_summary="Confidence adjusted using historical tool outcomes.",
    )
