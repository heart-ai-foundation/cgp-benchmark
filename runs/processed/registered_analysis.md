# Registered Analysis Results

This file reports the preregistered contrasts from the frozen analysis plan using `runs/processed/run_level_metrics.csv`. Exact tests are used where the data are sparse. The primary confirmatory dataset is Claude Code plus Aider; Codex plus Gemini CLI are reported as a companion extension.

## Primary

Runs: 72; paired baseline-CGP comparisons: 36.

### H1 / M1: Scope Drift Count

Baseline total scope-drift count: 0. CGP total scope-drift count: 1. Exact paired Wilcoxon two-sided p value: 1.0000.

### H3 / M3: Verification-Command Compliance

Baseline rate: 100.0%. CGP rate: 91.7%. Exact McNemar two-sided p value: 0.2500.

### M5: Verification Success

Baseline rate: 100.0%. CGP rate: 91.7%. Exact McNemar two-sided p value: 0.2500.

## Extension

Runs: 72; paired baseline-CGP comparisons: 36.

### H1 / M1: Scope Drift Count

Baseline total scope-drift count: 1. CGP total scope-drift count: 0. Exact paired Wilcoxon two-sided p value: 1.0000.

### H3 / M3: Verification-Command Compliance

Baseline rate: 100.0%. CGP rate: 100.0%. Exact McNemar two-sided p value: not defined.

### M5: Verification Success

Baseline rate: 100.0%. CGP rate: 100.0%. Exact McNemar two-sided p value: not defined.

## All Planned

Runs: 144; paired baseline-CGP comparisons: 72.

### H1 / M1: Scope Drift Count

Baseline total scope-drift count: 1. CGP total scope-drift count: 1. Exact paired Wilcoxon two-sided p value: 1.0000.

### H3 / M3: Verification-Command Compliance

Baseline rate: 100.0%. CGP rate: 95.8%. Exact McNemar two-sided p value: 0.2500.

### M5: Verification Success

Baseline rate: 100.0%. CGP rate: 95.8%. Exact McNemar two-sided p value: 0.2500.

## Interpretation Boundary

The registered H1 scope-drift endpoint does not show a favorable reduction. In the primary dataset, baseline scope drift was zero, so the endpoint was at a floor. Completion, non-submission, and evidence-trio findings remain important operational observations, but they must be reported according to their registered or exploratory status rather than as proof of drift reduction.
