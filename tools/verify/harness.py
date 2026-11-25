"""Shared helpers for the solution checks in tools/verify.

Every check loads the ```python blocks straight out of a note, executes them,
and compares the result with a brute force or a known answer, so a note can
never drift away from code that actually works.
"""
import contextlib
import io
import re
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
# Fences may be indented when they sit inside a Markdown list item.
CODE_RE = re.compile(r"^([ \t]*)```python[ \t]*\n(.*?)^\1```", re.S | re.M)
CASES = {}


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build_tree(vals):
    """LeetCode level-order list (None = missing) -> root."""
    if not vals or vals[0] is None:
        return None
    nodes = [None if v is None else TreeNode(v) for v in vals]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    return root


def tree_to_list(root):
    """Root -> LeetCode level-order list without trailing Nones."""
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        out.append(node.val if node else None)
        if node:
            queue += [node.left, node.right]
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root, val):
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val == val:
            return node
        stack += [node.left, node.right]
    return None


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_py(head, limit=10_000):
    out = []
    while head and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


def case(key):
    def deco(fn):
        CASES[key] = fn
        return fn
    return deco


def lc_path(num):
    hits = [p for p in REPO.rglob(f"{num}.*.md") if ".git" not in p.parts]
    if len(hits) != 1:
        raise FileNotFoundError(f"{num}: expected 1 file, found {hits}")
    return hits[0]


def blocks_of(path):
    text = Path(path).read_text(encoding="utf-8")
    return [textwrap.dedent(body) for _, body in CODE_RE.findall(text)]


def ns_from(code):
    ns = {"__name__": "lc", "TreeNode": TreeNode, "ListNode": ListNode}
    exec(compile(code, "<md>", "exec"), ns)
    return ns


def lc(num):
    """Namespace from the LAST python block of LeetCode note <num>."""
    blocks = blocks_of(lc_path(num))
    if not blocks:
        raise ValueError(f"{num}: no python block")
    return ns_from(blocks[-1])


def lc_all(num, name):
    """Namespaces of every python block of note <num> that defines `name`."""
    found = []
    for code in blocks_of(lc_path(num)):
        ns = ns_from(code)
        if name in ns:
            found.append(ns)
    if not found:
        raise ValueError(f"{num}: no block defines {name}")
    return found


def run_program(code, stdin_text):
    old_stdin = sys.stdin
    sys.stdin = io.TextIOWrapper(io.BytesIO(stdin_text.encode()))
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(code, "<prog>", "exec"), {"__name__": "__main__"})
    finally:
        sys.stdin = old_stdin
    return out.getvalue().strip()
