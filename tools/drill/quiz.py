"""`review.py quiz`: read a problem statement, name the pattern, check yourself.

The title is hidden because titles often give the pattern away ("Sliding Window Maximum").
About 30 seconds a card: this trains the step interviews punish most, recognising the pattern.
"""
import textwrap

from drill.picks import folder_of, weight
from drill.sections import signal, statement


def candidates(notes, read=lambda n: n.path.read_text(encoding="utf-8")):
    """(note, statement, signal) for every note that has a problem statement."""
    out = []
    for note in notes:
        text = read(note)
        body = statement(text)
        if body:
            out.append((note, body, signal(text)))
    return out


def draw(pool, count, rng):
    pool = list(pool)
    chosen = []
    while pool and len(chosen) < count:
        item = rng.choices(pool, weights=[weight(p[0]) * (2 if p[0].status == "🔄" else 1) for p in pool])[0]
        pool.remove(item)
        chosen.append(item)
    return chosen


def answer(note, sig):
    tags = f" · tags: {', '.join(note.tags)}" if getattr(note, "tags", ()) else ""
    lines = [f"→ #{note.number} {note.title} ({note.difficulty}) · pattern: {folder_of(note).replace('_', ' ')}{tags}"]
    if sig:
        lines.append(textwrap.fill(f"  signal: {sig}", width=100, subsequent_indent="          "))
    return "\n".join(lines)


def run(cards, today, ask=input, out=print, interactive=True):
    """Show each card; return quiz records [{date, number, ok}] (empty when not interactive)."""
    results = []
    for i, (note, body, sig) in enumerate(cards, 1):
        out(f"\n— Card {i}/{len(cards)} ({note.difficulty}) —\n{body}\n")
        if not interactive:
            continue
        ask("Your pattern (Enter to reveal): ")
        out(answer(note, sig))
        ok = ask("Did you name it? [y/N] ").strip().lower().startswith("y")
        results.append({"date": today.isoformat(), "number": note.number, "ok": ok})
    if not interactive:
        out("\n— Answers —")
        for i, (note, _, sig) in enumerate(cards, 1):
            out(f"{i}. " + answer(note, sig))
    return results
