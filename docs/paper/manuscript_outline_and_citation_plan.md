# Manuscript Outline and Citation Plan

This document is the next scientific-writing workflow artifact after the initial results snapshot. It converts the processed benchmark findings into a section-by-section paper plan and identifies the external literature needed to support the manuscript.

## Working Title

Drift Reduction Through Continuity-Governed Prompting: A Controlled Benchmark of Agent-Assisted Coding Workflows

## Core Claim

Continuity-Governed Prompting improved composite run validity and auditability across a controlled agent-assisted coding benchmark. The strongest empirical effect was not a large reduction in classic file-scope drift, which was rare in both conditions, but a reduction in invalid runs caused by non-submission and evidence failure, especially for Aider.

## Paper Structure

### Abstract

The abstract should state the operational problem, the preregistered benchmark design, the primary and companion datasets, the main validity rates, and the interpretation that CGP functions as an operational control layer. The abstract should avoid overclaiming "drift reduction" as only file-boundary drift and instead describe improved run validity, auditability, and task engagement.

Key result sentences:

Baseline prompting produced 56 valid runs out of 72 across all agents, while CGP produced 68 valid runs out of 72. In the primary preregistered dataset, baseline validity was 58.3% and CGP validity was 88.9%. The largest platform-specific effect was observed for Aider, where baseline validity was 16.7% and CGP validity was 77.8%.

### Introduction

The introduction should frame the problem as continuity failure in agent-assisted software work. Existing agent benchmarks primarily evaluate whether models can resolve issues or complete tasks, but production workflows also require continuity of scope, state, verification, and evidence across handoffs. The gap is that most prompt and benchmark designs evaluate output success without separately measuring whether the agent remained bound to an operational contract.

The introduction should cite current software-engineering agent benchmarks and agent-evaluation work. SWE-bench is the anchor citation for repository-level coding-agent evaluation. SWE-Gym and related coding-agent training/evaluation work can support the claim that agent scaffolds and trajectories matter. MLE-bench and AgentBench can support the broader point that agent evaluation increasingly includes tool use, long-horizon tasks, and environment interaction rather than isolated text generation.

End the introduction with the preregistered research question: whether a governance scaffold with explicit state, scope, non-goals, stop condition, verification, and evidence requirements improves run validity relative to ordinary task prompting.

### Methods

The methods section should be highly reproducible and should read as a benchmark protocol. It should describe:

The controlled benchmark repository, the six tasks, the two prompt conditions, the primary and companion agent sets, the deterministic run plans, the worktree isolation strategy, and the raw artifact capture procedure. It should define the primary analysis set as the 144 planned runs and explicitly state that eight archived harness-defect records were preserved but excluded.

The outcome definitions need special care. Scope drift is the narrow file-boundary metric. Run validity is the composite operational endpoint: work submitted, no scope drift, verification success, and CGP evidence completion when applicable. This distinction is central because the observed effect is more about run validity and non-submission than about frequent classic scope drift.

### Results

The results section should proceed from global to specific. First, report all-agent baseline versus CGP outcomes. Second, report primary preregistered outcomes. Third, report companion extension outcomes. Fourth, report failure-mode composition.

The Aider result should be presented as the clearest platform-sensitive effect: baseline Aider submitted valid work in only 3 of 18 runs, while CGP was valid in 14 of 18. Claude Code and Codex were ceiling performers. Gemini CLI was near ceiling, with one baseline scope-drift event.

### Discussion

The discussion should interpret CGP as a governance control layer rather than as a model capability improvement. The strongest finding is that explicit operational scaffolding can make agent behavior more auditable and more likely to produce a valid run. The study supports a consulting-relevant claim: organizations using coding agents need not rely only on better base models; they can improve reliability by controlling the work envelope, evidence requirements, and stop conditions.

The discussion should also acknowledge that the primary hypothesis name emphasizes drift reduction, while the observed data show rare file-scope drift. This is not a contradiction if the paper clearly distinguishes file-scope drift from broader prompting drift or continuity drift. The paper should say that CGP reduced invalidity and non-submission more strongly than it reduced already-rare file drift.

### Limitations

Limitations should include the controlled toy repository, small number of tasks, repeated use of the same task set, model/version volatility, possible CLI-specific behavior, and the composite nature of run validity. The paper should also note that some baseline runs passed verification despite doing no work, which shows that verification commands alone can be insufficient when task success depends on documentation or other changes not covered by tests.

### Figures and Tables

Figure 1 should show the benchmark pipeline: task specification, condition prompt, isolated worktree, agent execution, capture, verification, metrics, and evidence trio.

Figure 2 should show validity rate by agent and condition.

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

The next prose revision should strengthen Methods first, because the paper's credibility depends on transparent run inclusion, invalid-run handling, and outcome definitions. Results should remain closely tied to generated CSV outputs. The Introduction should be expanded only after the citation list is finalized, so claims about prior work are anchored to specific sources.
