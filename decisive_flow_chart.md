# MCP Preflight Advisor — Decision Flow

This server provides **advisory guidance** for tool usage.
It does **not** execute tools, block actions, or use ML.

Below is the full decision flow for a single `preflight_advice` call.

---

## 1. Entry Point (MCP Tool)

**File:** `server.py`
**Function:** `preflight_advice(input: AdvisoryInput)`

### Example Input (from MCP client)

```json
{
  "task_description": "Parse and summarize a malformed JSON file",
  "available_tools": ["filesystem.read", "json.parse"],
  "domain": "data-processing",
  "constraints": ["untrusted-input"]
}
```

### Responsibility

* Accept structured input from an AI agent
* Delegate all reasoning to the advisory engine
* Return a structured advisory response

⬇️

---

## 2. Advisory Orchestration Spine

**File:** `advisor/engine.py`
**Function:** `advise(input: AdvisoryInput)`

### Responsibility

* Coordinate all advisory signals
* Combine rules, history, risk, and similarity
* Produce a single explainable response

This function **does not reason itself**.
It composes decisions from specialized components.

⬇️

---

## 3. Deterministic Rule Evaluation (No History)

**File:** `advisor/rules.py`
**Function:** `apply_rules(input)`

### Inputs Used

* `task_description`
* `available_tools`

### Output

* initial `ToolSuggestion[]`
* early `AdvisoryWarning[]`
* explanation text

### Example Output (internal)

```python
ToolSuggestion(
  tool_name="filesystem.read",
  confidence=0.6,
  rationale="Default-first-tool heuristic (Phase 1 rule)."
)
```

This stage answers:

> “Given *only what I see now*, what tools look reasonable?”

⬇️

---

## 4. Historical Confidence Adjustment

**File:** `advisor/scoring.py`
**Function:** `adjust_confidence_with_history(...)`

### Inputs Used

* tool name
* historical tool outcomes

**Data Source**

* `SQLiteAdvisoryMemory.tool_stats(tool_name)`

### Logic (High Level)

* Require minimum sample size
* Blend rule confidence with historical success rate
* Never allow history to dominate

### Example Adjustment

| Tool       | Base Confidence | Historical Success | Adjusted |
| ---------- | --------------- | ------------------ | -------- |
| json.parse | 0.6             | 20%                | 0.45     |

This stage answers:

> “Have we actually seen this tool work before?”

⬇️

---

## 5. Outcome-Aware Risk Warnings

**File:** `advisor/risk.py`
**Function:** `risk_warnings_for_tool(tool_name, memory)`

### Inputs Used

* tool outcome counts (success vs failure)

### Example Warning Emitted

```json
{
  "code": "HISTORICAL_FAILURE_BIAS",
  "message": "Tool 'json.parse' has failed 5 out of 6 recorded uses.",
  "severity": "high"
}
```

This stage answers:

> “Is there evidence this tool is risky?”

⬇️

---

## 6. Similarity-Lite Task Matching (No ML)

**File:** `advisor/similarity.py`
**Functions:**

* `similarity_score(current, past)`
* `find_similar_tasks(...)`

### Signals Used

* domain match
* constraint overlap
* shared tools
* keyword overlap (string match only)

### Output (Optional)

* Similar past task references

### Example Evidence Summary

```text
Found 2 similar past tasks.
Most recent outcome: failure.
```

This stage answers:

> “Have we seen *this kind of situation* before?”

⬇️

---

## 7. Global Confidence Calculation

**File:** `advisor/scoring.py`
**Function:** `compute_overall_confidence(...)`

### Inputs Used

* adjusted tool confidences
* warning severities

### Behavior

* warnings reduce confidence
* absence of suggestions → low confidence
* result is always explicit

⬇️

---

## 8. Advisory Response Assembly

**File:** `advisor/engine.py`
**Function:** `advise(...)`

### Final Output (Returned to MCP Client)

```json
{
  "suggested_sequence": [
    {
      "tool_name": "filesystem.read",
      "confidence": 0.52,
      "rationale": "Default-first-tool heuristic (Phase 1 rule)."
    }
  ],
  "overall_confidence": 0.32,
  "warnings": [
    {
      "code": "HISTORICAL_FAILURE_BIAS",
      "message": "Tool 'json.parse' has failed 5 out of 6 recorded uses.",
      "severity": "high"
    }
  ],
  "explanation": "Applied Phase 1 heuristic: suggest first available tool.",
  "evidence_summary": "Found similar past tasks with negative outcomes."
}
```

This response is:

* advisory only
* deterministic
* explainable
* uncertainty-aware

⬇️

---

## 9. Observability (Out-of-Band)

**File:** `advisory_logging.py`
**Function:** `log_advisory(...)`

* Logs decision details to **STDERR**
* Never interferes with MCP JSON output
* Used for debugging, demos, and audits

---

## 10. Memory & Persistence (Background Layer)

**File:** `storage/sqlite_memory.py`
**Class:** `SQLiteAdvisoryMemory`

### Responsibilities

* Persist task records
* Track per-tool outcomes
* Enable similarity + confidence adjustment
* Survive restarts

No inference.
No mutation of history.
Append-only institutional memory.

---

## One-Sentence Flow Summary

> **Rules propose → history tempers → risk warns → similarity contextualizes → confidence is computed → advice is returned, never enforced.**

---
