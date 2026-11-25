"""Interview_Prep: every SQL result block matches SQLite's output; every OOP example runs."""
import re
import sqlite3

from harness import REPO, blocks_of, case

PREP = REPO / "Interview_Prep"
SQL_RE = re.compile(r"```sql\n(.*?)```\s*(?:\*\*Result\*\*\s*```text\n(.*?)```)?", re.S)


def fmt(value):
    if value is None:
        return "NULL"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def run_sql(schema, query):
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    statements = [s.strip() for s in query.split(";") if s.strip()]
    for statement in statements[:-1]:
        con.execute(statement)
    cur = con.execute(statements[-1])
    header = " | ".join(d[0] for d in cur.description)
    return "\n".join([header] + [" | ".join(fmt(v) for v in row) for row in cur.fetchall()])


@case("SQL")
def _(h):
    pairs = SQL_RE.findall((PREP / "SQL.md").read_text(encoding="utf-8"))
    schema = pairs[0][0]
    checked = 0
    for query, expected in pairs[1:]:
        assert expected, f"query without a Result block:\n{query}"
        got = run_sql(schema, query)
        assert got == expected.strip(), f"\n{query}\nexpected:\n{expected}\ngot:\n{got}"
        checked += 1
    assert checked >= 14, checked


@case("OOP")
def _(h):
    blocks = blocks_of(PREP / "OOP.md")
    assert len(blocks) >= 5
    for code in blocks:
        exec(compile(code, "<OOP.md>", "exec"), {"__name__": "oop"})  # each block asserts its own claims
