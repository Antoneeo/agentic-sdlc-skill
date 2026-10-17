# Catalogue delivery — review packet

## Assignment
Review the implementation for readiness against the original user need and the
design, applying the supplied methodology. Return READY or NOT_READY, the
substantive findings with evidence, and the single most useful next test (input,
expected observable output, and why). Do not edit files or execute code. Label
static deductions and checks not performed. The packet contains the complete
synthetic system; there are no other application modules to search.

## Original user need
A reader requests a catalogue or a summary. Deliver the complete available
records as text. A legitimately empty catalogue is a valid empty delivery.
Failed or unfinished reads must not be presented as completed. Stop takes
precedence. This increment has no network, permissions, persistence or retries.

## Design supplied for review
Two producers feed a shared publication boundary. The gate classifies explicit
success, failure, or unknown. Only success may publish; unknown and failure
block. Stop is checked first. Record content is joined with newlines.
The existing smoke tests cover delivery, failure and Stop. Assess whether the
increment is ready; the design and test results are evidence to assess.

## Implementation
```python
from copy import deepcopy

def read_catalogue(records):
    """A complete read uses records + complete; there is no status field."""
    return {"records": deepcopy(records), "complete": True}

def read_summary(records):
    """This producer uses the older explicit-status protocol."""
    return {"records": deepcopy(records), "status": "success"}

def classify_outcome(command, result):
    if not isinstance(result, dict):
        return "unknown"
    if result.get("status") in ("error", "failed"):
        return "failed"
    if result.get("status") == "success":
        return "success"
    return "unknown"

def deliver(command, result, *, classify=classify_outcome, stopped=False):
    """Publication boundary; incomplete results must not be called complete."""
    if stopped:
        return {"state": "stopped", "content": None}
    outcome = classify(command, result)
    if outcome != "success":
        return {"state": "blocked", "content": None}
    return {"state": "delivered", "content": "\n".join(result["records"])}
```

## Existing smoke tests
```python
from fixture import deliver, read_summary

assert deliver("read_summary", read_summary(["Atlas"])) == {"state": "delivered", "content": "Atlas"}
assert deliver("read_summary", {"status": "failed", "records": []}) == {"state": "blocked", "content": None}
assert deliver("read_summary", read_summary(["Atlas"]), stopped=True) == {"state": "stopped", "content": None}
print("3 existing smoke assertions passed")

```
