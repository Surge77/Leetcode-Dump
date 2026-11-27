"""Every note's optimized solution must reproduce LeetCode's official examples.

official_examples.json holds only the examples' inputs and expected outputs, read from each 'Example'
block of LeetCode's public problem pages (rebuild: see the PR that added it). This catches the one error
the brute-vs-optimized checks cannot: both solutions misreading the problem the same way.

* "any order" problems are compared as multisets (order ignored at every level).
* "return any valid answer" problems whose output differs from the listed one are skipped here:
  their own @case checks the answer with a validator.
"""
import json
import math
from pathlib import Path

from harness import build_list, build_tree, case, find_node, lc, list_to_py, tree_to_list

DATA = json.loads((Path(__file__).parent / "official_examples.json").read_text(encoding="utf-8"))
# Interactive or randomized problems, or inputs that encode pointers (cycles, shared tails, random links).
SPECIAL = {"116", "117", "138", "141", "278", "297", "374", "380", "427", "528"}
POINTER_TYPES = {"TreeNode", "ListNode"}
# LeetCode accepts these in any order although the statement does not say so.
ANY_ORDER = {"126", "212", "282", "336"}
# Several outputs are valid (e.g. any height-balanced BST); the note's own @case validates them.
ANY_ANSWER = {"108"}
# Arguments LeetCode's metadata types as integers but that are really nodes of the first (tree) argument.
NODE_ARGS = {"235": (1, 2), "236": (1, 2), "863": (1,)}


def convert(value, kind, tree=None):
    if kind == "TreeNode":
        if isinstance(value, int) and tree is not None:  # p, q, target, ... are nodes of `tree` given by value
            return find_node(tree, value)
        return build_tree(value)
    if kind == "ListNode":
        return build_list(value)
    if kind in ("list<ListNode>", "ListNode[]"):
        return [build_list(v) for v in value]
    return value


def convert_args(values, kinds):
    args, tree = [], None
    for value, kind in zip(values, kinds):
        arg = convert(value, kind, tree)
        if kind == "TreeNode" and tree is None:
            tree = arg
        args.append(arg)
    return args


def plain(value, kind=""):
    """Harness objects -> JSON-comparable values (an empty list or tree is [])."""
    if value is None and kind in POINTER_TYPES:
        return []
    if hasattr(value, "next") and hasattr(value, "val") and not hasattr(value, "left"):
        return list_to_py(value)
    if hasattr(value, "left") and hasattr(value, "val"):
        return tree_to_list(value)
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def same(got, want):
    if isinstance(want, float) or isinstance(got, float):
        return (isinstance(got, (int, float)) and isinstance(want, (int, float))
                and math.isclose(got, want, rel_tol=1e-5, abs_tol=1e-5))
    if isinstance(want, list) and isinstance(got, list):
        return len(got) == len(want) and all(same(g, w) for g, w in zip(got, want))
    return got == want


def canonical(value):
    if isinstance(value, list):
        return sorted((canonical(v) for v in value), key=repr)
    return value


def accept(num, entry, got, want):
    """True = matches; None = a different but possibly valid answer (checked by the note's own @case)."""
    any_order = entry["any_order"] or num in ANY_ORDER
    if same(got, want) or (any_order and same(canonical(got), canonical(want))):
        return True
    return None if entry["any_answer"] or num in ANY_ANSWER else False


def run_function(num, entry):
    ns = lc(int(num))
    for example in entry["cases"]:
        args = convert_args([json.loads(t) for t in example["input"]], entry["params"])
        for i in NODE_ARGS.get(num, ()):
            args[i] = find_node(args[0], args[i])
        want = json.loads(example["output"])
        result = getattr(ns["Solution"](), entry["method"])(*args)
        if entry["return"] == "TreeNode" and isinstance(want, int):  # e.g. LCA: the example shows the node's value
            got = result.val if result is not None else None
        elif entry["return"] == "void":
            got = plain(args[0], entry["params"][0])
        else:
            got = plain(result, entry["return"])
        verdict = accept(num, entry, got, want)
        assert verdict is not False, f"{num} {entry['method']}{tuple(example['input'])}: expected {want}, got {got}"


def run_design(num, entry):
    ns = lc(int(num))
    for example in entry["cases"]:
        ops, args = (json.loads(t) for t in example["input"])
        want = json.loads(example["output"])
        obj = ns[ops[0]](*convert_args(args[0], entry["constructor"]))
        got: list = [None]
        for op, a in zip(ops[1:], args[1:]):
            got.append(plain(getattr(obj, op)(*convert_args(a, entry["methods"].get(op, [])))))
        assert same(got, want), f"{num} design: expected {want}, got {got}"


def make(num, entry):
    @case(f"{num}-official")
    def _(h):
        (run_design if entry["kind"] == "design" else run_function)(num, entry)


for _num, _entry in DATA.items():
    if _num not in SPECIAL:
        make(_num, _entry)
