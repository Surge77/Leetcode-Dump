"""Assemble a random 3-question paper (Easy, Medium, Hard) from three different mock tests.

    python tools/judge/paper.py            # new paper
    python tools/judge/paper.py --seed 42  # the same paper again

Sitting a fixed mock twice tests memory, not skill; a shuffled paper does not.
"""
import argparse
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from judge import REPO, all_keys, problem  # noqa: E402

EXAM_HOURS = 3
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, help="reproduce a paper")
    args = parser.parse_args(argv)
    seed = args.seed if args.seed is not None else random.randrange(10**6)
    paper = pick(all_keys(), random.Random(seed))

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
