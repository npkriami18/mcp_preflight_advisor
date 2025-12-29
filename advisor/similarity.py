def similarity_score(current: dict, past: dict) -> int:
    score = 0

    if current.get("domain") and current["domain"] == past.get("domain"):
        score += 3

    shared_constraints = set(current.get("constraints", [])) & set(
        past.get("constraints", [])
    )
    score += len(shared_constraints) * 2

    shared_tools = set(current.get("tools", [])) & set(past.get("tools", []))
    score += len(shared_tools)

    for word in current.get("task", "").lower().split():
        if word in past.get("task", "").lower():
            score += 1
            break  # cap keyword effect

    return score

def find_similar_tasks(current: dict, history: list[dict], min_score: int = 4):
    scored = []

    for past in history:
        score = similarity_score(current, past)
        if score >= min_score:
            scored.append((score, past))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [task for _, task in scored[:3]]
