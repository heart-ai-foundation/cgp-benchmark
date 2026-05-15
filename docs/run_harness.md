# Run Harness

The run harness is the operational procedure for executing the preregistered 72-run benchmark after OSF preregistration.

## Pre-Run Gates

- OSF preregistration is public and recorded in `docs/osf_preregistration/submission_record.md`.
- `runs/run_plan.csv` exists and passes `python scripts/generate_run_plan.py --check`.
- Task start tags `task-1-start` through `task-6-start` exist.
- The benchmark app smoke checks pass:
  - `python -m pytest` from `benchmark-repo/`
  - `npm test` from `benchmark-repo/`
- Protocol check passes:
  - `node next-prompt-protocols/tools/sync-protocols.mjs --check`

## Execution Boundary

Generating the run plan and creating task start tags are not data collection. Data collection begins when the first assigned agent receives the first assigned run prompt.

## Run Plan

The deterministic run plan is generated with:

```bash
python scripts/generate_run_plan.py
```

The check command is:

```bash
python scripts/generate_run_plan.py --check
```

The plan uses seed `20260515`, randomizes task order within each agent platform, and randomizes condition order within each task-agent pair.

## Raw Records

Each run should leave raw material under `runs/raw/`, including:

- prompt used
- transcript or interaction log where available
- command log
- git diff
- verification outcome
- timing record
- token or telemetry export where available
- evidence trio for CGP runs

Processed metrics belong under `runs/processed/`.

## Preparing One Run

To preview a planned run prompt without creating run artifacts:

```bash
python scripts/prepare_run.py --run-id task-1-claude-code-cgp-r1 --dry-run
```

To prepare a run directory:

```bash
python scripts/prepare_run.py --run-id task-1-claude-code-cgp-r1
```

By default, `prepare_run.py` also creates an isolated git worktree under `worktrees/` at the task start tag:

```bash
worktrees/task-1-claude-code-cgp-r1
```

Use `--worktree-root PATH` only when the worktree should be created somewhere other than `worktrees/`. Use `--no-worktree` only for prompt/metadata generation without an execution workspace.

For CGP runs, `prepare_run.py` also replaces the repository-level scaffold with a run-specific scaffold and commits that setup inside the isolated worktree. The run-specific scaffold records the task start tag as its commit anchor; the run metadata records `metrics_base_commit` after scaffold setup. Drift metrics should compare final agent output against `metrics_base_commit`, not against the raw task start tag. This prevents scaffold installation from contaminating scope-drift measurement.

CGP run scaffolds include evidence trio paths in `notes/`, `runs/`, and `evidence/`. These paths are part of the CGP allowed-files set for M4 scaffold-adherence measurement. Scope-drift scoring for CGP runs should treat the evidence trio as allowed operational evidence, while task-code drift remains visible through changed-file categories.

Running `prepare_run.py` creates setup artifacts only. The benchmark observation begins when the assigned agent receives the generated prompt.

## Invalid Run Handling

If a run exposes a harness defect before or during execution, preserve its raw artifacts and mark it invalid. Do not reinterpret it as a valid benchmark observation. The corrected run should use the original planned `run_id` after the harness is fixed, with the invalid attempt retained separately or marked in metadata.
