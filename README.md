# CGP Drift Reduction Benchmark

Controlled benchmark suite for testing Continuity-Governed Prompting (CGP) against ordinary summary-based prompting in agent-assisted coding workflows.

Canonical repository target:

`github.com/heart-ai-foundation/cgp-benchmark`

## Status

Initial scaffold. The experiment design is locked in the Heart Corpus as `CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`; benchmark execution has not started.

## Repository Layout

- `benchmark-repo/` - controlled Python and JavaScript hybrid project used for task runs
- `next-prompt-protocols/` - reference scaffold for CGP condition
- `runs/raw/` - raw run logs, diffs, and telemetry exports
- `runs/processed/` - cleaned run data
- `analysis/` - reproducible analysis scripts
- `paper/` - demo paper source
- `docs/` - experiment protocol and task documentation
- `docs/osf_preregistration/` - OSF-ready pre-data preregistration packet
- `docs/run_harness.md` - post-preregistration execution procedure
- `docs/prompt_templates/` - Baseline and CGP condition prompt templates
- `runs/run_plan.csv` - deterministic randomized run order generated after OSF preregistration
- `scripts/prepare_run.py` - prepares a single run prompt and optional isolated worktree

## License

Code is licensed under MIT. Paper, protocol text, and data are intended for CC BY 4.0 publication unless a specific file states otherwise.
