"""One-field intervention; asserts the causal link, not a proposed fix."""
import json

from fixture import deliver, read_catalogue, read_summary


payload = read_catalogue(["Atlas", "Orion"])
untouched = deliver("read_catalogue", payload)
with_status = deliver("read_catalogue", {**payload, "status": "success"})
summary = read_summary(["Atlas", "Orion"])
without_status = deliver("read_summary", {k: v for k, v in summary.items() if k != "status"})

assert untouched == {"state": "blocked", "content": None}
assert with_status == {"state": "delivered", "content": "Atlas\nOrion"}
assert without_status == {"state": "blocked", "content": None}
print(json.dumps({"unchanged": untouched, "added_status_only": with_status,
                  "removed_status_only": without_status}, indent=2))
