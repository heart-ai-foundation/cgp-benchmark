# Experiment Protocol

This repository implements the controlled benchmark described in `CGP_Drift_Reduction_Benchmarking_Experiment_Design_v1_1.md`.

The locked design specifies:

- 6 tasks
- 2 conditions: baseline summary prompting and CGP via Next-Prompt Protocol
- 2 agent platforms: Claude Code and Aider
- 3 replications per cell
- 72 total runs

Primary metrics:

- M1: scope drift count
- M2: reproducibility variance
- M3: verification command compliance

Secondary and exploratory metrics are defined in the design document. This file is a repository-local orientation surface, not a replacement for the locked Heart Corpus experiment design.
