# Phase 0 CGP Evidence Trio Correction

## Why this exists

The first attempted CGP benchmark run exposed a harness defect: the run-specific CGP scaffold did not require the evidence trio, so the agent could complete the coding task while M4 evidence-trio completeness failed for an implementation reason rather than an agent adherence reason.

The attempted run must be treated as invalid harness validation, not as benchmark data. Before any rerun, the harness must require evidence artifacts in the run-specific active protocol and provide stable evidence paths.

## Macro delta alignment

This slice reduces the gap between preregistered CGP measurement and executable benchmark operation by making M4 measurable through the scaffold itself.

## Next objective

Update the run preparation harness so CGP runs include explicit evidence trio requirements, stable evidence artifact paths, and prompt text that instructs the agent to write those artifacts before completion. Mark the first attempted run as invalid due to harness defect without rerunning any benchmark cells in this slice.

## Files in play

- `scripts/prepare_run.py` - generate run-specific evidence paths and active protocol requirements.
- `docs/run_harness.md` - document invalid-run and evidence-trio handling.
- `runs/raw/task-1-claude-code-cgp-r1/**` - mark prior attempt invalid.
- `next-prompt-protocols/**` - protocol rotation and sync state.

## Non-goals

- Do not rerun `task-1-claude-code-cgp-r1` during this correction slice.
- Do not run any new benchmark cells.
- Do not alter the registered OSF preregistration.
- Do not reinterpret the invalid attempted run as valid benchmark evidence.

## Acceptance

- `python scripts/prepare_run.py --run-id task-1-claude-code-cgp-r1 --dry-run` shows explicit evidence trio requirements.
- A temporary CGP worktree preparation produces `notes/`, `runs/`, and `evidence/` paths in the run-specific active protocol.
- `python scripts/generate_run_plan.py --check` passes.
- `python -m pytest` passes from `benchmark-repo/`.
- `npm test` passes from `benchmark-repo/`.
- `node next-prompt-protocols/tools/sync-protocols.mjs --check` passes from repository root.
