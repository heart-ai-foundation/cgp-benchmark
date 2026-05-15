# CGP Drift Reduction Benchmark

This OSF project preregisters a controlled benchmark of Continuity-Governed Prompting (CGP) for agent-assisted coding workflows.

The study tests whether CGP, operationalized through the Next-Prompt Protocol scaffold, reduces scope drift, improves handoff reproducibility, and increases verification-command compliance relative to ordinary summary-based prompting.

No benchmark data collection has begun at the time this packet is prepared. Repository validation checks have only confirmed that the controlled benchmark codebase runs and that the protocol scaffold synchronizes.

The canonical public repository is:

`https://github.com/heart-ai-foundation/cgp-benchmark`

The locked design document is:

`CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`

Primary hypotheses:

- H1: CGP reduces scope drift relative to summary-based prompting.
- H2: CGP improves handoff reproducibility, measured as lower variance across replications.
- H3: CGP increases verification-command compliance.

Exploratory hypothesis:

- H4: CGP may change token consumption and wall-clock time; direction is not predicted.

The experiment will run 72 total cells: 6 tasks, 2 prompting conditions, 2 agent platforms, and 3 replications per cell.
