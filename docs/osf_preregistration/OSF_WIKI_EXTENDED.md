# CGP Drift Reduction Benchmark

This OSF project preregisters a controlled benchmark of Continuity-Governed Prompting (CGP) for agent-assisted coding workflows.

The study tests whether CGP, operationalized through the Next-Prompt Protocol scaffold, reduces scope drift, improves handoff reproducibility, and increases verification-command compliance relative to ordinary summary-based prompting.

The canonical public repository is:

`https://github.com/heart-ai-foundation/cgp-benchmark`

The primary preregistered design document is:

`CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`

The primary preregistered run plan is:

`runs/run_plan.csv`

The primary benchmark contains 72 planned cells:

- 6 benchmark tasks
- 2 prompting conditions: baseline and Continuity-Governed Prompting
- 2 agent platforms: Claude Code and Aider
- 3 replications per task-condition-agent cell

Operational note: Aider is included in the primary preregistered run plan. Aider was installed and version-checked before Aider rows were executed, and Aider runs are handled by the same prepare, isolated worktree, transcript, capture, metrics, and commit workflow used for the other agent platforms.

Primary hypotheses:

- H1: CGP reduces scope drift relative to summary-based prompting.
- H2: CGP improves handoff reproducibility, measured as lower variance across replications.
- H3: CGP increases verification-command compliance.

Exploratory hypothesis:

- H4: CGP may change token consumption and wall-clock time; direction is not predicted.

## Companion Multi-Agent Extension

This project also records a companion extension to evaluate whether the CGP effect generalizes across additional coding-agent platforms. The extension preserves the same tasks, prompt conditions, replication count, run capture structure, and outcome measures as the primary benchmark.

The extension agent platforms are:

- Codex
- Gemini CLI

The extension run plan is separate from the primary preregistered run plan:

`runs/agent_extension_run_plan.csv`

The extension contains 72 planned companion cells:

- 6 benchmark tasks
- 2 prompting conditions: baseline and Continuity-Governed Prompting
- 2 additional agent platforms: Codex and Gemini CLI
- 3 replications per task-condition-agent cell

Primary data from Claude Code and Aider remain the preregistered confirmatory dataset. Codex and Gemini CLI results should be reported as a companion or amended multi-agent analysis unless a formal OSF amendment explicitly designates them as part of an expanded confirmatory analysis.

Each run uses an isolated git worktree and records a generated prompt, run metadata, transcript, git diff, metrics file, and verification record. CGP runs additionally require an evidence trio: a design note, an operational run record, and a machine-readable evidence JSON file. Invalid runs and harness-defect runs are preserved rather than silently discarded or reinterpreted.

The purpose of the extension is external validity. If CGP reduces drift across multiple agent platforms, that supports the claim that continuity governance is a portable control pattern. If results differ by platform, those differences will identify where governance scaffolds transfer cleanly and where tool-specific adaptation is required.
