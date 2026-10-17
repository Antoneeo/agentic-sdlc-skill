"""Synthetic catalogue delivery system. No Eclosion code or external services.

The baseline deliberately contains a producer/consumer contract mismatch.
The reference variant is an experimental positive control, not a product fix.
"""
from copy import deepcopy


def read_catalogue(records):
    """A complete read uses records + complete; there is no status field."""
    return {"records": deepcopy(records), "complete": True}


def read_summary(records):
    """This producer uses the older explicit-status protocol."""
    return {"records": deepcopy(records), "status": "success"}


def baseline_outcome(command, result):
    if not isinstance(result, dict):
        return "unknown"
    if result.get("status") in ("error", "failed"):
        return "failed"
    if result.get("status") == "success":
        return "success"
    return "unknown"


def reference_outcome(command, result):
    """Use each producer's declared contract; absence of error is insufficient."""
    if not isinstance(result, dict):
        return "unknown"
    if result.get("status") in ("error", "failed"):
        return "failed"
    records = result.get("records")
    if not isinstance(records, list) or any(type(r) is not str for r in records):
        return "unknown"
    if command == "read_catalogue":
        return "success" if result.get("complete") is True else "unknown"
    if command == "read_summary":
        return "success" if result.get("status") == "success" else "unknown"
    return "unknown"


def deliver(command, result, *, classify=baseline_outcome, stopped=False):
    """Publication boundary; incomplete results must not be called complete."""
    if stopped:
        return {"state": "stopped", "content": None}
    outcome = classify(command, result)
    if outcome != "success":
        return {"state": "blocked", "content": None}
    return {"state": "delivered", "content": "\n".join(result["records"])}
