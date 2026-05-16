# Submission Package

## Working Title

Reliability and Auditability Effects of Continuity-Governed Prompting: A Controlled Benchmark of Agent-Assisted Coding Workflows

## Author

Dylan D. Mobley, Heart AI Foundation.

## Corresponding Author

Dylan D. Mobley.

## Article Type

Empirical software-engineering benchmark / methods evaluation.

## Package Inventory

Main manuscript:

- `docs/paper/manuscript_draft.md`

Figures:

- `docs/paper/figures/graphical_abstract.svg`
- `docs/paper/figures/figure1_benchmark_pipeline.svg`
- `docs/paper/figures/figure2_validity_by_agent_condition.png`
- `docs/paper/figures/figure2_validity_by_agent_condition.svg`
- `docs/paper/figures/figure3_invalid_run_mechanisms.png`
- `docs/paper/figures/figure3_invalid_run_mechanisms.svg`

Tables:

- `docs/paper/tables/table1_summary_by_dataset_agent_condition.md`
- `docs/paper/tables/table2_invalid_run_mechanisms.md`

Captions:

- `docs/paper/figure_and_table_captions.md`

References:

- `docs/paper/references.bib`

Preregistration and deviation record:

- OSF registration: `https://osf.io/fnmg5`
- `docs/osf_preregistration/OSF_PREREGISTRATION.md`
- `docs/osf_preregistration/locked_design/CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`
- `docs/research_integrity/CGP_Benchmark_Preregistration_Deviation_Note_v1_1.md`

Data and analysis:

- `runs/processed/run_level_metrics.csv`
- `runs/processed/summary_by_condition.csv`
- `runs/processed/summary_by_dataset_condition.csv`
- `runs/processed/summary_by_dataset_agent_condition.csv`
- `runs/processed/summary_by_task_agent_condition.csv`
- `runs/processed/registered_analysis.md`
- `runs/processed/registered_analysis.json`
- `scripts/analyze_results.py`
- `scripts/run_registered_analysis.py`
- `scripts/generate_paper_assets.py`

Raw records:

- `runs/raw/`
- `runs/raw/invalid/`

## Required Submission Notes

The paper should be submitted or posted under the reliability-and-auditability title, not under the original drift-reduction title. The registered primary endpoint was scope drift count and returned a null result at a baseline floor. Composite run validity, work submission, non-submission, and evidence production are operational findings, not confirmatory registered endpoints.

The OSF preregistration body should remain unchanged. The v1.1 deviation note should be attached or linked as a supplemental deviation record.

## Open Items Before Preprint/PDF

1. Confirm that `CGP_Benchmark_Preregistration_Deviation_Note_v1_1.md` has been added to OSF as a supplemental record.
2. Follow the preprint-first strategy in `docs/paper/venue_strategy.md`.
3. Complete the checks in `docs/paper/preprint_checklist.md`.
4. Convert citations from Pandoc citation syntax to the target venue style if needed.
5. Generate the final PDF or LaTeX package after installing a renderer or choosing a venue template.
