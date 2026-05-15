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
