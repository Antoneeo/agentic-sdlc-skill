from fixture import deliver, read_summary

assert deliver("read_summary", read_summary(["Atlas"])) == {"state": "delivered", "content": "Atlas"}
assert deliver("read_summary", {"status": "failed", "records": []}) == {"state": "blocked", "content": None}
assert deliver("read_summary", read_summary(["Atlas"]), stopped=True) == {"state": "stopped", "content": None}
print("3 existing smoke assertions passed")
