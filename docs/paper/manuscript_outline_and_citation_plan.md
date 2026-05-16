# Manuscript Outline and Citation Plan

This document is the next scientific-writing workflow artifact after the initial results snapshot. It converts the processed benchmark findings into a section-by-section paper plan and identifies the external literature needed to support the manuscript.

## Working Title

Reliability and Auditability Effects of Continuity-Governed Prompting: A Controlled Benchmark of Agent-Assisted Coding Workflows

## Core Claim

The registered primary endpoint, scope drift count, returned a null result at a baseline floor. Continuity-Governed Prompting improved composite run validity and auditability across a controlled agent-assisted coding benchmark, but this should be framed as valid completion, non-submission detection, and evidence production rather than as demonstrated drift reduction. The strongest empirical effect was concentrated in Aider, where invalid runs caused by non-submission were common under baseline prompting and much less common under CGP.

## Paper Structure

### Abstract

The abstract should state the operational problem, the preregistered benchmark design, the primary and companion datasets, the null result on the registered drift endpoint, the main validity rates, and the interpretation that CGP functions as an operational control layer. It should not claim drift reduction. It should describe improved run validity, auditability, and task engagement as the operative observed findings.

Key result sentences:

The registered primary endpoint was scope drift. In the primary preregistered dataset, baseline prompting produced 0 scope-drift events and CGP produced 1, with exact paired Wilcoxon two-sided p = 1.0000. Across all planned runs, baseline and CGP each produced 1 scope-drift event.

Baseline prompting produced 56 valid runs out of 72 across all agents, while CGP produced 68 valid runs out of 72. In the primary preregistered dataset, baseline validity was 58.3% and CGP validity was 88.9%. The largest platform-specific effect was observed for Aider, where baseline validity was 16.7% and CGP validity was 77.8%.

### Introduction

The introduction should frame the problem as continuity failure in agent-assisted software work. Existing agent benchmarks primarily evaluate whether models can resolve issues or complete tasks, but production workflows also require continuity of scope, state, verification, and evidence across handoffs. The gap is that most prompt and benchmark designs evaluate output success without separately measuring whether the agent remained bound to an operational contract.

The introduction should cite current software-engineering agent benchmarks and agent-evaluation work. SWE-bench is the anchor citation for repository-level coding-agent evaluation. SWE-Gym and related coding-agent training/evaluation work can support the claim that agent scaffolds and trajectories matter. MLE-bench and AgentBench can support the broader point that agent evaluation increasingly includes tool use, long-horizon tasks, and environment interaction rather than isolated text generation.

End the introduction with the preregistered research question: whether a governance scaffold with explicit state, scope, non-goals, stop condition, verification, and evidence requirements reduces scope drift and improves operational reliability relative to ordinary task prompting. The final paragraph should foreshadow that the drift endpoint was null at floor while reliability and auditability findings remained informative.

### Methods

The methods section should be highly reproducible and should read as a benchmark protocol. It should describe:

The controlled benchmark repository, the six tasks, the two prompt conditions, the primary and companion agent sets, the deterministic run plans, the worktree isolation strategy, and the raw artifact capture procedure. It should define the primary analysis set as the 144 planned runs and explicitly state that eight archived harness-defect records were preserved but excluded.

The outcome definitions need special care. Scope drift is the registered primary file-boundary metric. Run validity is the composite operational endpoint: work submitted, no scope drift, verification success, and CGP evidence completion when applicable. This distinction is central because the observed effect is about run validity and non-submission, not about frequent classic scope drift.

### Results

The results section should proceed from registered endpoint to operational findings. First, report H1/M1 scope drift and the null floor effect. Second, report registered verification compliance and verification success. Third, report all-agent baseline versus CGP validity outcomes as operational findings. Fourth, report primary preregistered outcomes, companion extension outcomes, and failure-mode composition.

The Aider result should be presented as the clearest platform-sensitive effect: baseline Aider submitted valid work in only 3 of 18 runs, while CGP was valid in 14 of 18. Claude Code and Codex were ceiling performers. Gemini CLI was near ceiling, with one baseline scope-drift event.

### Discussion

The discussion should interpret CGP as a governance control layer rather than as a model capability improvement. The strongest defensible finding is that explicit operational scaffolding can make agent behavior more auditable and more likely to produce a valid run in a baseline-unreliable platform. The study supports a consulting-relevant claim: organizations using coding agents need not rely only on better base models; they can improve reliability by controlling the work envelope, evidence requirements, and stop conditions.

The discussion must state plainly that the primary registered drift hypothesis was not supported. The paper should avoid reframing the null as success by redefining drift after observing the data. It can state that CGP reduced invalidity and non-submission in the observed benchmark while the file-scope drift endpoint was untestable at the baseline floor.

### Limitations

Limitations should include the floor effect on the registered drift endpoint, ceiling effects in three of four platforms, effect concentration in one platform, the controlled toy repository, small number of tasks, repeated use of the same task set, model/version volatility, possible CLI-specific behavior, and the composite nature of run validity. The paper should also note that some baseline runs passed verification despite doing no work, which shows that verification commands alone can be insufficient when task success depends on documentation or other changes not covered by tests.

### Figures and Tables

Figure 1 should show the benchmark pipeline: task specification, condition prompt, isolated worktree, agent execution, capture, verification, metrics, and evidence trio.

Figure 2 should show validity rate by agent and condition, labeled as an operational validity figure rather than evidence of drift reduction.

Figure 3 should show invalid-run mechanisms by agent and condition, separating non-submission, scope drift, verification failure, and evidence incompleteness.

Table 1 should report summary metrics by dataset, agent, and condition using `runs/processed/summary_by_dataset_agent_condition.csv`.

Table 2 should report invalid-run mechanisms using `runs/processed/run_level_metrics.csv`.

## Citation Targets

SWE-bench should be cited as the central repository-level software-engineering benchmark for language models and coding agents.

SWE-Gym should be cited for the importance of software-engineering agent trajectories and training/evaluation scaffolds.

MLE-bench should be cited as an example of evaluating agents in realistic machine-learning engineering environments with tool use and benchmark scaffolds.

AgentBench should be cited for the broader movement from text-only evaluation toward interactive agent benchmarks across environments.

Repository-level and multilingual coding-agent benchmarks such as ML-Bench and SWE-PolyBench should be considered for the related-work section if the paper needs a broader benchmark landscape.

Self-reflection and agent-scaffold papers should be reviewed selectively. They are relevant only if the paper distinguishes CGP from internal self-reflection: CGP is not asking the model to introspect; it is imposing an external governance contract and evidence boundary.

## Drafting Priorities

The next prose revision should strengthen Results first around the registered endpoint and exact-test outputs, then Methods around run inclusion, invalid-run handling, and outcome definitions. Results should remain closely tied to generated CSV outputs and `runs/processed/registered_analysis.md`. The Introduction should be expanded only after the citation list is finalized, so claims about prior work are anchored to specific sources.
