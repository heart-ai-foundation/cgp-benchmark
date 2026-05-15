# Archived Pilot Runs - Interactive Claude Code

The following observations were collected with interactive Claude Code operation before the production harness was upgraded to automated print-mode execution:

- `task-1-claude-code-cgp-r1`
- `task-1-claude-code-baseline-r1`
- `task-1-claude-code-cgp-r2`
- `task-1-claude-code-baseline-r2`
- `task-1-claude-code-cgp-r3`
- `task-1-claude-code-baseline-r3`

These records remain under `runs/raw/_pilot_interactive/` for auditability and harness-debug provenance, but they are archived as pilot/debug observations and should not be pooled with production observations unless the analysis plan explicitly models execution mode.

Production data collection should use one consistent execution mode. Beginning after this archive note, Claude Code production runs should use the automated print-mode wrapper:

```bash
python scripts/run_claude_code_print.py --run-id RUN_ID --commit --push
```
