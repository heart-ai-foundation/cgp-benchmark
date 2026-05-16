# Results Snapshot

This snapshot was generated from `runs/processed/run_level_metrics.csv` after excluding archived harness-defect records under `runs/raw/invalid/`. The processed analysis includes 144 completed planned runs: 72 primary runs from Claude Code and Aider, and 72 companion extension runs from Codex and Gemini CLI. Eight archived harness-defect records are preserved but excluded from the planned-run analysis.

Across all agents and both datasets, baseline prompting produced 56 valid runs out of 72, for a validity rate of 77.8%. Continuity-Governed Prompting produced 68 valid runs out of 72, for a validity rate of 94.4%. Work submission was also higher under CGP: 100.0% of CGP runs submitted work, compared with 79.2% of baseline runs. Verification success was high in both conditions, with 100.0% under baseline and 95.8% under CGP. Scope drift was rare in both conditions, occurring in 1 of 72 baseline runs and 1 of 72 CGP runs.

In the primary preregistered dataset, baseline prompting produced 21 valid runs out of 36, for a validity rate of 58.3%. Continuity-Governed Prompting produced 32 valid runs out of 36, for a validity rate of 88.9%. This primary contrast is strongly shaped by Aider: Aider baseline runs were valid in 3 of 18 cases, while Aider CGP runs were valid in 14 of 18 cases. Claude Code completed all primary baseline and CGP runs validly.

In the companion extension dataset, baseline prompting produced 35 valid runs out of 36, for a validity rate of 97.2%. Continuity-Governed Prompting produced 36 valid runs out of 36. Codex completed all extension runs validly in both conditions. Gemini CLI completed all CGP extension runs validly and had one invalid baseline run due to scope drift into `benchmark-repo/tests/test_config.py`.

The most common invalid-run mechanism was not classic scope drift. In Aider baseline runs, many invalid observations reflected non-submission: the agent completed without changing files. These records are retained as invalid benchmark outcomes because the assigned task was not performed. CGP substantially reduced this non-submission pattern for Aider, though some Aider CGP runs still failed because of task verification failures or incomplete/misplaced evidence files.

CGP evidence-trio completeness was high. Across all CGP runs, 71 of 72 had complete evidence trios, for a completeness rate of 98.6%. In the primary dataset, 35 of 36 CGP runs had complete evidence trios. In the extension dataset, all 36 CGP runs had complete evidence trios.

## Key Tables

### Overall by Condition

| Condition | n | Valid n | Valid rate | Work submitted | Task success | Scope drift any | Evidence trio complete |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 72 | 56 | 77.8% | 79.2% | 100.0% | 1.4% | n/a |
| CGP | 72 | 68 | 94.4% | 100.0% | 95.8% | 1.4% | 98.6% |

### By Dataset and Condition

| Dataset | Condition | n | Valid n | Valid rate | Work submitted | Task success | Scope drift any | Evidence trio complete |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | Baseline | 36 | 21 | 58.3% | 58.3% | 100.0% | 0.0% | n/a |
| Primary | CGP | 36 | 32 | 88.9% | 100.0% | 91.7% | 2.8% | 97.2% |
| Extension | Baseline | 36 | 35 | 97.2% | 100.0% | 100.0% | 2.8% | n/a |
| Extension | CGP | 36 | 36 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% |

### By Agent and Condition

| Dataset | Agent | Condition | n | Valid n | Valid rate | Work submitted | Task success | Scope drift any | Evidence trio complete |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | Aider | Baseline | 18 | 3 | 16.7% | 16.7% | 100.0% | 0.0% | n/a |
| Primary | Aider | CGP | 18 | 14 | 77.8% | 100.0% | 83.3% | 5.6% | 94.4% |
| Primary | Claude Code | Baseline | 18 | 18 | 100.0% | 100.0% | 100.0% | 0.0% | n/a |
| Primary | Claude Code | CGP | 18 | 18 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% |
| Extension | Codex | Baseline | 18 | 18 | 100.0% | 100.0% | 100.0% | 0.0% | n/a |
| Extension | Codex | CGP | 18 | 18 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% |
| Extension | Gemini CLI | Baseline | 18 | 17 | 94.4% | 100.0% | 100.0% | 5.6% | n/a |
| Extension | Gemini CLI | CGP | 18 | 18 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% |
