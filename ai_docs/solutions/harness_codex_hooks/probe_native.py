"""Read native Codex hook loading without granting trust or starting a model turn."""
import json
import os
from pathlib import Path
import queue
import subprocess
import threading

root = Path(__file__).resolve().parent
report = json.loads((root / "consumer_results.json").read_text(encoding="utf-8"))
binary = next((Path(os.environ["LOCALAPPDATA"]) / "OpenAI/Codex/bin").glob("*/codex.exe"))
env = dict(os.environ, CODEX_HOME=report["codex_home"])
p = subprocess.Popen([str(binary), "app-server", "--stdio"], cwd=report["project"],
                     env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
messages = queue.Queue()
def read():
    for line in p.stdout:
        messages.put(json.loads(line))
threading.Thread(target=read, daemon=True).start()
def send(value):
    p.stdin.write(json.dumps(value) + "\n")
    p.stdin.flush()
def response(identifier):
    while True:
        value = messages.get(timeout=30)
        if value.get("id") == identifier:
            assert "error" not in value, value
            return value
try:
    send({"id": 1, "method": "initialize", "params": {
        "clientInfo": {"name": "f091_probe", "version": "1"},
        "capabilities": {"experimentalApi": True}}})
    initialized = response(1)
    send({"method": "initialized"})
    send({"id": 2, "method": "hooks/list", "params": {"cwds": [report["project"]]}})
    result = {"initialize": initialized, "hooks_list": response(2)}
    (root / "native_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
finally:
    p.terminate()
    p.wait(timeout=10)
