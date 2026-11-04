"""Native hooks before an offline turn: no external model endpoint or trust bypass."""
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

here = Path(__file__).resolve().parent
repo = here.parents[2]
project = repo.parent / "f091-native-session-fixture"
(project / "ai_docs").mkdir(parents=True, exist_ok=True)
(project / "ai_docs/README.md").write_text("F091_NATIVE_ORIENTATION_MARKER\n", encoding="utf-8")
binary = Path(r"C:\Users\apint\AppData\Local\OpenAI\Codex\bin\a159911ff70742e9\codex.exe")
env = dict(os.environ, CODEX_HOME=r"C:\Users\apint\.codex")
p = subprocess.Popen([str(binary), "-c", 'model_provider="f091_offline"',
                      "-c", 'model="f091-offline"', "-c",
                      'model_providers.f091_offline={name="Offline hook acceptance",base_url="http://127.0.0.1:9/v1",wire_api="responses",requires_openai_auth=false,request_max_retries=0,stream_max_retries=0}',
                      "app-server", "--stdio"], cwd=project, env=env,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                     text=True, encoding="utf-8")
messages = queue.Queue()
events = []
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
            return value
        events.append(value)
try:
    send({"id": 1, "method": "initialize", "params": {
        "clientInfo": {"name": "f091_native_acceptance", "version": "1"},
        "capabilities": {"experimentalApi": True}}})
    initialized = response(1)
    assert "error" not in initialized, initialized
    send({"method": "initialized"})
    send({"id": 2, "method": "hooks/list", "params": {"cwds": [str(project)]}})
    listed = response(2)
    assert "error" not in listed, listed
    entry = listed["result"]["data"][0]
    hooks = [{key: h.get(key) for key in ["eventName", "statusMessage", "enabled", "trustStatus"]}
             for h in entry["hooks"]]
    send({"id": 3, "method": "thread/start", "params": {
        "cwd": str(project), "ephemeral": True, "sandbox": "read-only",
        "modelProvider": "f091_offline", "model": "f091-offline",
        "config": {"model_providers": {"f091_offline": {
            "name": "Offline hook acceptance", "base_url": "http://127.0.0.1:9/v1",
            "wire_api": "responses", "requires_openai_auth": False,
            "request_max_retries": 0, "stream_max_retries": 0}}}}})
    started = response(3)
    turn = None
    if "result" in started:
        thread_id = started["result"]["thread"]["id"]
        send({"id": 4, "method": "turn/start", "params": {
            "threadId": thread_id,
            "input": [{"type": "text", "text": "F091 native hook fixture. Do not use tools."}]}})
        turn = response(4)
    deadline = time.monotonic() + 12
    while time.monotonic() < deadline:
        try:
            events.append(messages.get(timeout=0.3))
        except queue.Empty:
            pass
    serialized = json.dumps(events)
    result = {"hooks": hooks, "discovery_errors": entry["errors"],
              "discovery_warnings": entry["warnings"],
              "ephemeral_thread_started": "result" in started,
              "thread_error": started.get("error"),
              "turn_error": turn.get("error") if turn else None,
              "notification_methods": sorted({x.get("method", "") for x in events}),
              "orientation_marker_seen": "F091_NATIVE_ORIENTATION_MARKER" in serialized,
              "reminder_marker_seen": "agentic-sdlc: first decide" in serialized,
              "hook_events": [{"method": x.get("method"),
                               "event": (x.get("params", {}).get("run") or {}).get("eventName"),
                               "status": (x.get("params", {}).get("run") or {}).get("status")}
                              for x in events if x.get("method", "").startswith("hook/")],
              "offline_turn_requested": turn is not None,
              "external_model_endpoint": False, "trust_store_edited": False}
    assert result["orientation_marker_seen"] and result["reminder_marker_seen"], result
    completed = {x["event"] for x in result["hook_events"] if x["status"] == "completed"}
    assert {"sessionStart", "userPromptSubmit"} <= completed, result
    (here / "native_start_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
finally:
    p.terminate()
    p.wait(timeout=10)
