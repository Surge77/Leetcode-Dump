"""The drill's progress file, tools/review_state.json.

It is committed, so progress follows you across machines. One note (or one cold/quiz record) per line
keeps git diffs and merges readable.
"""
import json
import os
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parents[1] / "review_state.json"
VERSION = 2
LISTS = ("cold", "quiz")


def empty():
    return {"version": VERSION, "notes": {}, "cold": [], "quiz": []}


def load_state(path=STATE_FILE):
    if not path.exists():
        return empty()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise SystemExit(f"{path} is not valid JSON ({err}). Fix it by hand (a git merge conflict?) "
                         "or restore it with `git checkout -- tools/review_state.json`.")
    if isinstance(data, dict) and "version" not in data and all(k.isdigit() for k in data):
        data = migrate_v1(data)
    if not isinstance(data, dict) or data.get("version") != VERSION:
        raise SystemExit(f"{path}: expected a version {VERSION} state file, got version {data.get('version')!r}")
    state = empty()
    state.update(data)
    return state


def migrate_v1(notes):
    """v1 was {number: {streak, due, history: ["2026-11-26:pass", ...]}}: keep streaks and due dates."""
    migrated = {}
    for number, entry in notes.items():
        history = []
        for item in entry.get("history", []):
            day, _, outcome = item.partition(":")
            history.append({"date": day, "grade": "ok" if outcome == "pass" else "fail"})
        streak = int(entry.get("streak", 0))
        migrated[number] = {"step": streak, "streak": streak, "due": entry["due"], "history": history}
    return {**empty(), "notes": migrated}


def dumps(state):
    def block(name, rows, closing):
        if not rows:
            return [f' "{name}": {"{}" if closing == "}" else "[]"}']
        return [f' "{name}": {"{" if closing == "}" else "["}', ",\n".join(rows), f" {closing}"]

    notes = sorted(state["notes"].items(), key=lambda kv: int(kv[0]))
    parts = [f' "version": {VERSION}']
    parts.append("\n".join(block("notes", [f'  "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in notes], "}")))
    for name in LISTS:
        rows = [f"  {json.dumps(r, ensure_ascii=False)}" for r in state[name]]
        parts.append("\n".join(block(name, rows, "]")))
    return "{\n" + ",\n".join(parts) + "\n}\n"


def save_state(state, path=STATE_FILE):
    """Write atomically: an interrupted save never leaves a truncated state file."""
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(dumps(state), encoding="utf-8", newline="\n")
    os.replace(tmp, path)
