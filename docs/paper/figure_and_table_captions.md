# Figure and Table Captions

## Figure 1

Benchmark run-capture pipeline. Each benchmark run began with a task specification containing allowed files and verification commands, then proceeded through either a baseline prompt or a CGP prompt that added manifest, lock, stop-condition, and evidence-trio requirements. Runs were executed in isolated git worktrees, captured as transcripts and diffs, and scored into run-level metrics. CGP evidence files were treated as allowed operational evidence when computing scope drift.

## Figure 2

Operational run validity by agent and prompt condition. Bars show the proportion of runs classified as valid under the operational composite endpoint for each agent platform and prompt condition. A run was classified as valid when work was submitted, scope drift count was zero, verification passed, and, for CGP runs, the evidence trio was complete. This figure should not be interpreted as the registered primary drift endpoint; registered scope drift was analyzed separately and returned a null result at a baseline floor.

## Figure 3

Invalid-run mechanisms by agent and prompt condition. Bars count invalid planned runs by observed failure mechanism. The dominant failure mode was non-submission in Aider baseline runs, where the agent completed without changing files while repository verification still passed. CGP eliminated Aider non-submission in this benchmark but did not eliminate all failures, including verification failures and one incomplete or misplaced evidence record.

## Table 1

Summary by dataset, agent, and condition. The table reports planned-run counts, operational validity counts and rates, work-submission rates, task-verification success rates, scope-drift incidence, and CGP evidence-trio completeness. Primary rows correspond to the preregistered Claude Code and Aider dataset. Extension rows correspond to the companion Codex and Gemini CLI dataset and should be interpreted as external-validity evidence rather than as a replacement for the preregistered primary analysis.

## Table 2

Invalid-run mechanisms. The table enumerates invalid planned runs by dataset, agent, prompt condition, and failure mechanism. The table supports the central operational interpretation that the strongest observed effect involved prevention of non-submission and improved evidence production, not demonstrated reduction of the registered scope-drift endpoint.
