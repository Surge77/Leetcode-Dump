# Note prose v2 backfill (in progress)

Phase 2 of note format v2: rewrite every note's v1 prose sections into the interview-ready sections of
[the template](../../LeetcodeTemplates/ActiveTemplate.md): Recognition Signal, Clarifying Questions, Approach Ladder,
Why It Works, Dry Run, Test Cases, Bugs to Watch, Follow-ups & Variations, Related. The first run on 2026-11-28 stopped
on the model's weekly usage limit before any batch was written.

## How to resume

1. For each `manifests/manifest_XX.json` (12 batches of ~39 notes), have one agent follow
   [INSTRUCTIONS.md](INSTRUCTIONS.md) and write `out/batch_XX.json`. In Claude Code:
   *"Follow tools/backfill/INSTRUCTIONS.md for manifest_05.json"*, one Sonnet subagent per manifest.
   Agents never edit notes; they only write JSON.
2. Apply and check:

   ```bash
   python tools/backfill/apply_prose_v2.py tools/backfill/out/batch_*.json --dry-run
   python tools/backfill/apply_prose_v2.py tools/backfill/out/batch_*.json
   python tools/build_index.py && python tools/verify/verify.py && python -m unittest discover -s tools/tests
   ```

   The applier refuses to write if any code block would change. Spot-check a few notes per batch for accuracy
   (complexities, dry-run traces, expected outputs) before committing.
3. When every note is done, delete this folder and make the v2 sections required in `tools/notebook/model.py`.

`sample_139.json` is a complete example entry (and the fixture for `tools/tests/test_backfill.py`).
