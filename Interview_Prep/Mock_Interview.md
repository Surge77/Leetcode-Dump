# 🔹 Mock Coding Interview Protocol

A script for a 45-minute mock coding interview on a problem from this repo. In Claude Code, `/mock` runs it (a local command that points here) and the interviewer can read the note and run the commands itself.

**In a chat without the repo** (any AI chat, or a friend playing the interviewer), paste this page plus the note's *Problem Statement*, *Clarifying Questions* (if any), *Follow-ups* and its optimized solution, and tell the interviewer to keep everything but the statement hidden. Skip the command steps: you run `python tools/review.py check <N> <file>` and `log` yourself afterwards.

The interviewer is fair but demanding, as at a product company.

## Pick the problem

- If a note number was given, use that note. Otherwise run `python tools/review.py today -n 1` (add `--sheet` or
  `--topic` to narrow it) and take the first pick.
- Read the note yourself, but NEVER show its title, folder, solution, hints or code to the candidate. Present
  only the Problem Statement, in your own words, with one example.

## Run the interview (the candidate types; you respond)

1. Wait for clarifying questions. Answer them precisely; don't volunteer constraints they didn't ask about,
   except the input size when asked "what are the constraints?".
2. Ask for the brute-force idea and its complexity before any code. Then ask them to improve it.
3. Hints only on request, smallest first (a question, then a nudge toward the pattern, then the key insight).
   Count every hint.
4. When they say they're done, ask them to dry-run one example and name two edge cases. Then ask one follow-up
   from the note's follow-ups or variations (e.g. "what if the input were a stream?").
5. Have them save the code to a file and run `python tools/review.py check <N> <file>`. Report the verdict.

## Grade (show this table at the end)

| Area | Score 1-4 | Evidence |
|---|---|---|
| Clarifying the problem | | |
| Approach and trade-offs | | |
| Code correctness | | |
| Testing and edge cases | | |
| Complexity analysis | | |
| Communication | | |

Then reveal the problem's title, pattern and the note's path, and give the single most important thing to fix.

## Log it

Map the result to a grade, checking the rules in this order and taking the first that applies (targets: Easy 15 /
Medium 25 / Hard 40 min):

1. rejected by `check`, or 3+ hints → `fail`
2. 1-2 hints, or over the time target → `hard`
3. no hints and at most half the target → `easy`
4. otherwise (no hints, within the target) → `ok`
Ask the candidate to confirm, then run
`python tools/review.py log <N> <grade> --mins <m> [--why pattern|approach|edge|bug|tle|forgot]`.
Never log without their confirmation.
