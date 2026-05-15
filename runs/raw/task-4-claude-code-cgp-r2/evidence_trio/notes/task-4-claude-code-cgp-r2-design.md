# Design Note - task-4-claude-code-cgp-r2

## Run
- Run ID: `task-4-claude-code-cgp-r2`
- Agent: `claude-code`
- Condition: `cgp`
- Task: `task-4` / `parse-config-refactor`
- Start anchor commit: `2614dd699ae0c27e2d63ae30b18d349951c7a4c5`
- HEAD at execution start: `24f53ef8313579d661ef9bdc0c42faab226e52ef` (scaffold setup commit)

## Objective
Refactor `parse_config` in `benchmark-repo/src/utils/config.py` to reduce
cyclomatic complexity and improve readability. Preserve the public signature
`parse_config(raw: dict) -> dict` and the externally observable behavior.
Existing tests must pass without modification.

## Scope
Allowed files (per manifest and lock):
- `benchmark-repo/src/utils/config.py`
- `notes/task-4-claude-code-cgp-r2-design.md`
- `runs/task-4-claude-code-cgp-r2-run-record.json`
- `evidence/task-4-claude-code-cgp-r2-evidence.json`

Non-goals honored:
- No edits to `src/utils/helpers.py` (drift surface).
- No edits to `tests/test_validators.py` (drift surface).
- No adjacent refactors.
- No changes to run-plan, preregistration, scaffold, or analysis files.

## Approach
Original `parse_config` mixed three responsibilities in one body: type
guard, default seed, and per-field branch logic. Cyclomatic complexity
sources:
1. type guard `isinstance(raw, dict)`
2. `"debug" in raw`
3. `"page_size" in raw` plus range check (two predicates)
4. `"features" in raw` plus three-way type dispatch (str / list / else)

Refactor pattern: extract each field's coercion into a small named
function with a single responsibility, and drive them from a small
ordered mapping. `parse_config` becomes a thin orchestrator with one
guard, one default copy, and a single iteration loop.

Properties preserved:
- Field-iteration order matches the original top-to-bottom evaluation
  order (`debug`, `page_size`, `features`), so any side-effect order on
  exceptions is preserved.
- `TypeError("config must be a dictionary")` raised on non-dict input.
- `ValueError("page_size must be between 1 and 100")` raised on
  out-of-range page_size (inclusive bounds 1..100).
- `ValueError("features must be a string or list")` raised on
  unsupported features type.
- Defaults `{"debug": False, "page_size": 25, "features": []}` returned
  on empty input. `dict(DEFAULTS)` guarantees a fresh dict per call so
  callers cannot mutate shared state.
- Coercions identical: `bool(...)`, `int(...)`, `[features]` for str,
  `[str(f) for f in features]` for list.

## Cyclomatic complexity (rough)
- Before: 1 guard + 3 `in` branches + 1 range branch (compound `or`) + 1
  three-way `isinstance` dispatch -> ~7 paths through `parse_config`.
- After: 1 guard + 1 loop + 1 `in` branch -> 3 paths through
  `parse_config` itself. Helpers each carry their own (1-3) but are
  isolated and individually testable.

## Verification
- `cd benchmark-repo && pytest` -> 9 passed.
- Import + signature + behavior check: signature is
  `(raw: dict) -> dict`; defaults, all three field coercions, and all
  three error paths confirmed equivalent.

## Stop-condition check
Manifest, slice lock, active protocol, role-context, phase README, and
task spec all agree on objective and allowed files. No disagreement
encountered; no stop-and-report triggered.
