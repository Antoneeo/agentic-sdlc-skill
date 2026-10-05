"""Freeze the two user-authorized Eclosion reports as dated design inputs."""
import datetime
import hashlib
import json
from pathlib import Path

out = Path(__file__).resolve().parent / "eclosion"
out.mkdir(exist_ok=True)
records = []
for name in ("TEST_m145_card_continuity.md", "REVIEW_m145_card_trace_core.md"):
    origin = Path("D:/SoftwareDev/chatPNT/ai_docs/audit/reviews") / name
    data = origin.read_bytes()
    target = out / name
    if target.exists() and target.read_bytes() != data:
        raise SystemExit("Existing snapshot differs; keep history and choose a new snapshot name.")
    target.write_bytes(data)
    records.append({"origin": str(origin), "snapshot": target.name,
                    "sha256": hashlib.sha256(data).hexdigest()})
manifest = {"captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "thread": "01a1007c-4bfa-76b1-a5c9-241baea23f86",
            "status": "Reports read; Eclosion tests not rerun here. Working checkout may have changed.",
            "sources": records}
(out / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
