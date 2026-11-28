"""Assemble a random 3-question paper (Easy, Medium, Hard) from three different mock tests.

    python tools/judge/paper.py            # new paper
    python tools/judge/paper.py --seed 42  # the same paper again
    python tools/judge/paper.py --final    # the held-out mocks: your last rehearsal, sit it once

Sitting a fixed mock twice tests memory, not skill; a shuffled paper does not. Mocks 8-10 are held out
of normal papers: keep them unopened until the week before the exam, then sit `--final` under a timer.
"""
import argparse
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from judge import REPO, all_keys, problem, utf8_stdout  # noqa: E402

EXAM_HOURS = 3
HOLDOUT = {"M8", "M9", "M10"}  # mock tests reserved for the final rehearsal
SLOTS = (("1", "Easy", "20–30 min"), ("2", "Medium", "50–60 min"), ("3", "Hard", "the rest"))


def pick(keys, rng):
    """One key per slot, each from a different mock test."""
    used_tests, paper = set(), []
    for slot, _, _ in SLOTS:
        options = [k for k in keys if k.endswith(f"Q{slot}") and k.split("Q")[0] not in used_tests]
        if not options:
            raise SystemExit("not enough mock tests to build a paper")
        key = rng.choice(options)
        used_tests.add(key.split("Q")[0])
        paper.append(key)
    return paper


def pool(keys, final):
    """Normal papers never use the held-out mocks; a --final paper uses only them."""
    return [k for k in keys if (k.split("Q")[0] in HOLDOUT) == final]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, help="reproduce a paper")
    parser.add_argument("--final", action="store_true", help="the held-out mocks 8-10 (sit once, last week)")
    args = parser.parse_args(argv)
    utf8_stdout()
    seed = args.seed if args.seed is not None else random.randrange(10**6)
    paper = pick(pool(all_keys(), args.final), random.Random(seed))

    start = datetime.now()
    end = start + timedelta(hours=EXAM_HOURS)
    print(f"Paper #{seed} — {EXAM_HOURS} hours: {start:%H:%M} → {end:%H:%M}\n")
    for key, (slot, difficulty, budget) in zip(paper, SLOTS):
        prob = problem(key)
        print(f"  Q{slot} {difficulty:<6} ({budget:>9})  {prob.statement.relative_to(REPO).as_posix()}")
    print("\nRules: read only the statements. Q1 fully → brute force for Q3 → Q2 → optimise Q3.")
    print("Judge each answer:")
    for key in paper:
        print(f"  python tools/judge/judge.py {key} my_{key.lower()}.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
