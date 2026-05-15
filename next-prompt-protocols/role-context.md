# Role Context - CGP Benchmark

## Read in this order

1. `.slice-lock.json`
2. `manifest.json`
3. `role-context.md`
4. `phases/<current-phase>/README.md`
5. `active/<current-protocol>.md`
6. Completed protocols only as background

## Source of truth

The source of truth is the locked Heart Corpus design document:

`CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`

Repository-local summaries in `docs/` are orientation surfaces only.

## Scope discipline

Stay inside `allowed_files`. Treat `non_goals` as closed unless Dylan explicitly changes the experiment design or repository objective.

## Verification rules

Run the exact verification commands named by the active protocol and manifest before declaring completion.

## Stop conditions

Stop when the manifest, slice lock, active protocol, code, or locked experiment design disagree on a load-bearing detail.
