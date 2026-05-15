# Phase 0 Run Plan and Task Tags

## Why this exists

The OSF preregistration is public and recorded. The next governed step is to create the auditable randomized run plan, prompt templates, run harness orientation, and task start tags before any agent benchmark runs begin.

## Macro delta alignment

This slice reduces the gap between preregistered design and executable benchmark operation by creating the materials needed to execute the 72-run design without yet collecting benchmark run data.

## Next objective

Add deterministic run-plan generation, validate the 72-run plan, document the run harness and prompt templates, and create/push the six task start tags after the run-plan commit.

## Files in play

- `README.md` - note run-plan and tag status.
- `docs/run_harness.md` - describe execution boundaries and generated artifacts.
- `docs/prompt_templates/baseline.md` - baseline condition prompt template.
- `docs/prompt_templates/cgp.md` - CGP condition prompt template.
- `runs/run_plan.csv` - randomized preregistered run order.
- `runs/run_plan_metadata.json` - seed and generation metadata.
- `scripts/generate_run_plan.py` - deterministic run-plan generator and checker.
- `next-prompt-protocols/**` - protocol rotation and sync state.

## Non-goals

- Do not run any agent benchmark cells.
- Do not create raw run logs or processed results.
- Do not draft results or interpret outcomes.
- Do not change the registered OSF preregistration content.

## Acceptance

- `python scripts/generate_run_plan.py --check` passes from repository root.
- `python -m pytest` passes from `benchmark-repo/`.
- `npm test` passes from `benchmark-repo/`.
- `node next-prompt-protocols/tools/sync-protocols.mjs --check` passes from repository root.
- Tags `task-1-start` through `task-6-start` exist and point to the run-plan commit.
