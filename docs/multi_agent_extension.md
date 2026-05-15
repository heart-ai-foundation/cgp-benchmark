# Multi-Agent Extension

The primary preregistered plan remains `runs/run_plan.csv`. The multi-agent extension is a companion benchmark for additional agent platforms and should be reported as an amendment or companion analysis unless separately preregistered.

Generate and validate the extension plan:

```bash
python scripts/generate_agent_extension_plan.py
python scripts/generate_agent_extension_plan.py --check
```

Run Gemini CLI extension cells:

```bash
python scripts/run_gemini_cli.py --next --commit --push
```

Gemini runs use `gemini` headless mode with `--approval-mode yolo`, `--skip-trust`, and `--output-format stream-json` by default. Output is streamed live, written under `runs/raw/RUN_ID/transcripts/`, and scanned for stop-condition language.

Before running benchmark cells, verify Gemini CLI authentication in the same terminal environment:

```bash
gemini -p "Return exactly OK" --approval-mode yolo --skip-trust --output-format json
```

If Gemini opens an authentication page or prompts for login, complete authentication first and rerun the smoke test before starting benchmark cells.

Parallel execution is possible as long as each process uses a distinct run ID and therefore a distinct worktree. For example, one terminal can continue the primary Claude Code plan while another terminal runs Gemini extension cells:

```bash
python scripts/run_claude_code_print.py --next --commit --push
python scripts/run_gemini_cli.py --next --commit --push
```

Do not run two processes for the same run ID.

Codex extension rows are included in `runs/agent_extension_run_plan.csv`; a Codex-specific runner should follow the same lifecycle before those rows are executed.
