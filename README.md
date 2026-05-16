# CGP Reliability and Auditability Benchmark

Controlled benchmark suite for testing Continuity-Governed Prompting (CGP) against ordinary summary-based prompting in agent-assisted coding workflows.

Canonical repository target:

`github.com/heart-ai-foundation/cgp-benchmark`

Manuscript DOI:

`10.5281/zenodo.20234367`

## Epistemic Status

The registered primary endpoint was scope drift. The completed primary dataset showed baseline scope drift at the floor: 0 baseline scope-drift events in the preregistered primary dataset, 1 CGP scope-drift event, and an exact paired Wilcoxon two-sided p value of 1.0000. Across all planned primary plus companion-extension runs, scope drift occurred once under baseline and once under CGP. This benchmark therefore does not support a claim that CGP reduced scope drift in this run.

The operative observed findings are reliability and auditability findings: valid completion improved from 56 of 72 baseline runs to 68 of 72 CGP runs across all planned runs, work submission improved from 79.2% to 100.0%, and CGP evidence-trio completeness was 71 of 72. These findings must be read under the preregistration deviation note:

`docs/research_integrity/CGP_Benchmark_Preregistration_Deviation_Note_v1_1.md`

The registered analysis output is:

`runs/processed/registered_analysis.md`

## Repository Layout

- `benchmark-repo/` - controlled Python and JavaScript hybrid project used for task runs
- `next-prompt-protocols/` - reference scaffold for CGP condition
- `runs/raw/` - raw run logs, diffs, and telemetry exports
- `runs/processed/` - cleaned run data
- `scripts/` - reproducible analysis and harness scripts
- `docs/paper/` - paper source, figures, tables, and references
- `docs/` - experiment protocol and task documentation
- `docs/osf_preregistration/` - OSF-ready pre-data preregistration packet
- `docs/research_integrity/` - preregistration deviation and remediation notes
- `docs/run_harness.md` - post-preregistration execution procedure
- `docs/prompt_templates/` - Baseline and CGP condition prompt templates
- `runs/run_plan.csv` - deterministic randomized run order generated after OSF preregistration
- `scripts/prepare_run.py` - prepares a single run prompt and optional isolated worktree

## License

Code is licensed under MIT. Paper, protocol text, and data are intended for CC BY 4.0 publication unless a specific file states otherwise.
