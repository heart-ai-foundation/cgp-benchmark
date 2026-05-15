# OSF Preregistration: CGP Drift Reduction Benchmark

## Title

Drift Reduction Through Continuity-Governed Prompting: A Controlled Benchmark of Agent-Assisted Coding Workflows

## Authors

Dylan D. Mobley, Heart AI Foundation.

## Research Question

Does Continuity-Governed Prompting (CGP), operationalized through the Next-Prompt Protocol scaffold, reduce scope drift, improve handoff reproducibility, and increase verification-command compliance in agent-assisted coding workflows relative to ordinary summary-based prompting?

## Study Type

Controlled software-engineering benchmark experiment.

## Registration Status

Pre-data preregistration. No benchmark run data has been collected. Repository smoke tests have been run only to validate that the controlled codebase and protocol scaffold are executable.

## Hypotheses

H1, the primary hypothesis, is that CGP reduces scope drift in agent-assisted coding workflows compared to ordinary summary-based prompting.

H2 is that CGP improves handoff reproducibility, measured as lower variance in agent behavior across replications of the same task.

H3 is that CGP increases verification-command compliance, measured as the rate at which agents run named verification commands before declaring completion.

H4 is exploratory. CGP may change token consumption and wall-clock time per completed task. The direction of this effect is not predicted, and increased cost or time is not interpreted as methodology failure because the methodology may intentionally trade operational overhead for drift reduction and verification discipline.

## Independent Variables

The experiment has four factors.

Condition has two levels: baseline summary-based prompting and CGP via the Next-Prompt Protocol scaffold.

Agent platform has two levels: Claude Code and Aider.

Task has six levels: input validation, user docstring, user-items endpoint, parse-config refactor, favorite-items feature, and LoginForm empty-password bug fix.

Replication has three levels per task, condition, and agent cell.

## Dependent Variables

Primary metrics are:

M1, scope drift count, defined as the number of files modified outside the allowed-files set per run.

M2, reproducibility variance, defined as variance in scope drift, completion success, and files touched across three replications of each task-agent-condition cell.

M3, verification-command compliance, defined as whether the agent executed the named verification command before declaring completion.

The CGP-only scaffold adherence metric is M4, evidence trio completeness, scored 0 to 3 based on structural presence of design note, run record, and evidence JSON.

Secondary metrics are M5, task verification success, and M8, human correction burden.

Exploratory metrics are M6, token cost per task; M7, wall-clock time per task; M9, clarification loops; M10, retry attempts; and M11, unauthorized file access if telemetry supports it.

## Sample Size

The study uses 72 total runs:

6 tasks x 2 conditions x 2 agents x 3 replications.

This is an initial controlled benchmark, not a full-scale field validation.

## Materials

The controlled benchmark codebase is published in `benchmark-repo/` of:

`https://github.com/heart-ai-foundation/cgp-benchmark`

The task specifications are in `docs/task_specs/`.

The CGP scaffold is in `next-prompt-protocols/`.

Raw run data will be published in `runs/raw/`. Processed run data will be published in `runs/processed/`. Analysis scripts will be published in `analysis/`. The paper source will be published in `paper/`.

## Procedure

For each run, the experimenter will clone or reset the benchmark repository to the task start tag. For CGP condition runs, the Next-Prompt Protocol scaffold will be installed or activated. For baseline runs, the agent will receive ordinary prose project context plus the task description.

The agent will work until it declares completion or hits a stop condition. The experimenter will record clarification loops, retry attempts, and human interventions. After the run, the experimenter will compute the changed file list, scope drift, verification-command compliance, verification success, evidence trio completeness for CGP runs, token usage if available, wall-clock time, and any available unauthorized file access telemetry.

Agent session state will be cleared between runs to reduce contamination.

## Randomization

For each task-agent pair, condition order will be randomized. Task order will also be randomized within each agent platform.

## Blinding

Full blinding is not feasible because the experimenter operates the agent. Bias mitigation relies on automated drift detection, automated verification execution, automated evidence completeness scoring, and telemetry-derived cost and timing where available.

## Inclusion and Exclusion Criteria

A run is included if it starts from the correct task tag, uses the assigned condition prompt, and reaches a declared completion or stop condition.

A run is excluded or flagged if the repository cannot be reset cleanly, the agent platform changes materially mid-run, required verification cannot run for environmental reasons unrelated to the agent output, or the condition prompt is accidentally mixed with the other condition. Exclusions and flags will be documented in the run record and final report.

## Analysis Plan

For M1, paired Wilcoxon signed-rank tests will compare Baseline and CGP conditions.

For M3 and M5, McNemar's test will compare paired binary outcomes.

For M2, variance ratios will compare reproducibility across conditions by task and agent cell.

Effect sizes and 95 percent bootstrapped confidence intervals will be reported. The significance threshold is alpha = 0.05 with Bonferroni correction for the three primary hypotheses.

M4 will be reported only within the CGP condition to characterize scaffold adherence and flag partial-compliance runs.

M6 through M11 will be reported descriptively as exploratory metrics and will not be used for primary hypothesis testing.

## Stop Conditions

The experiment halts and reports incomplete data if the benchmark codebase fails baseline verification, agent platform API limits prevent completion, an agent version change creates a material confound mid-experiment, or the CGP scaffold fails to install or synchronize correctly.

Per CGP doctrine, stop events are logged as evidence, not suppressed as failures.

## Data and Code Availability

Code, task specs, raw run data, processed data, analysis scripts, and paper source will be published at:

`https://github.com/heart-ai-foundation/cgp-benchmark`

Code is licensed under MIT. Paper, protocol text, and data are intended for CC BY 4.0 release unless a specific file states otherwise.

## Conflicts of Interest

The author developed CGP during production work on EMPI House / Dwell platform infrastructure and may have a financial interest through future commercial implementation services offered by HeartCore Ventures LLC. This interest will be disclosed with results. The methodology itself is published openly by the Heart AI Foundation.

## AI Assistance Disclosure

AI language models were used to help articulate and operationalize repository and preregistration materials. Experimental design decisions, hypothesis specifications, and methodological choices remain the author's responsibility.

## Deviations

Any deviation from this preregistration will be documented in run records and in the final paper. Deviations will not be retroactively described as preregistered.
