"""`review.py plan --by DATE`: how many new problems a day it takes to see every 🔄 note twice in time."""
import math
from datetime import timedelta

PACE_DAYS = 7
# A new note needs its first solve plus a review one day later before it can turn ✅,
# so it must be started at least this many days before the deadline.
LEAD_DAYS = 2


def started_on(entry):
    return entry["history"][0]["date"] if entry["history"] else None


def plan(notes, entries, today, deadline):
    """Return a dict of the numbers behind the plan (see `render`)."""
    days = (deadline - today).days
    if days < LEAD_DAYS:
        raise SystemExit(f"--by {deadline} is less than {LEAD_DAYS} days away")
    todo = [n for n in notes if n.status == "🔄"]
    not_started = [n for n in todo if str(n.number) not in entries]
    start_window = days - LEAD_DAYS + 1
    need = math.ceil(len(not_started) / start_window) if not_started else 0
    since = (today - timedelta(days=PACE_DAYS)).isoformat()
    in_scope = {str(n.number) for n in notes}
    recent_starts = sum(1 for k, e in entries.items() if k in in_scope and (started_on(e) or "") >= since)
    pace = recent_starts / PACE_DAYS
    finish = None
    if not_started and pace > 0:
        finish = today + timedelta(days=math.ceil(len(not_started) / pace))
    return {"days": days, "scope": len(notes), "solved": len(notes) - len(todo),
            "in_progress": len(todo) - len(not_started), "not_started": len(not_started),
            "need_per_day": need, "pace": pace, "finish_starting": finish,
            "last_start": deadline - timedelta(days=LEAD_DAYS)}


def render(p, deadline):
    lines = [f"Scope: {p['scope']} notes · ✅ {p['solved']} · in progress {p['in_progress']} · "
             f"not started {p['not_started']} · {p['days']} days to {deadline}"]
    if not p["not_started"]:
        lines.append("Every 🔄 note has been started: keep clearing the due reviews each day.")
        return "\n".join(lines)
    need = p["need_per_day"]
    lines.append(f"Start at least {need} new problem{'s' if need != 1 else ''} a day (last start {p['last_start']}); "
                 f"with their reviews that is about {2 * need} problems a day.")
    if p["pace"] == 0:
        lines.append(f"Last {PACE_DAYS} days: no new problems started.")
    else:
        verdict = "on track" if p["finish_starting"] <= p["last_start"] else "behind"
        lines.append(f"Last {PACE_DAYS} days: {p['pace']:.1f} new a day → all started by "
                     f"{p['finish_starting']} — {verdict}.")
    return "\n".join(lines)
